from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.utils.qr import generate_qr_code
from app.core.security import get_current_user, create_access_token
from app.core.config import settings
from app.models.user import User
from app.repository.qr_repository import QRRepository
from app.service.qr_service import QRService
from app.schemas.user import Token

router = APIRouter(prefix="/qr", tags=["qr"])


@router.post("/generate")
def generate_qr(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Генерирует QR-код для авторизации (возвращает PNG изображение)"""
    repo = QRRepository(db)
    service = QRService(repo)

    qr_session = service.generate_qr(current_user.id)

    # Генерируем реальное изображение QR-кода
    qr_image_bytes = generate_qr_code(qr_session.code)

    return Response(
        content=qr_image_bytes,
        media_type="image/png",
        headers={
            "X-QR-Code": qr_session.code,
            "X-Expires-At": str(qr_session.expires_at)
        }
    )


@router.post("/confirm", response_model=Token)
def confirm_qr(
    code: str,
    db: Session = Depends(get_db)
):
    """Подтверждение QR-кода и выдача JWT"""
    repo = QRRepository(db)
    service = QRService(repo)

    qr = service.confirm_qr(code)

    if not qr:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid, expired or already used QR code"
        )

    access_token = create_access_token(
        data={"sub": str(qr.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": qr.user_id
    }