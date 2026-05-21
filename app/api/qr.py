from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.qr import generate_qr_code
from app.schemas.user import QRLoginData, Token
from app.core.security import create_access_token
from app.service.auth_service import AuthService
from app.repository.user_repository import UserRepository
from datetime import timedelta
from app.core.config import settings

router = APIRouter(prefix="/qr", tags=["qr"])

@router.get("/generate")
async def generate_qr(username: str):
    """Генерирует QR-код с username для быстрого логина"""
    qr_bytes = generate_qr_code(username)
    return Response(content=qr_bytes, media_type="image/png")


@router.post("/login", response_model=Token)
async def qr_login(login_data: QRLoginData, db: Session = Depends(get_db)):
    """Логин через код из QR (пока по username)"""
    repo = UserRepository(db)
    service = AuthService(repo)
    
    user = repo.get_by_username(login_data.code)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Создаём токен
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}