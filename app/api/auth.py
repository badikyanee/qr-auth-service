from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.service.auth_service import AuthService
from app.repository.user_repository import UserRepository
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


# -----------------------------
# SIGNUP
# -----------------------------
@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)

    try:
        user = service.signup(user_data.username, user_data.password)
        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    service = AuthService(repo)

    user = service.authenticate(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }