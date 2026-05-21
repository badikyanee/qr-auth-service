from passlib.context import CryptContext
from app.repository.user_repository import UserRepository

# Используем pbkdf2_sha256 — современный и без ограничения 72 байта
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def signup(self, username: str, password: str):
        if self.repo.get_by_username(username):
            raise ValueError("User with this username already exists")
        
        hashed_password = pwd_context.hash(password)
        return self.repo.create(username, hashed_password)

    def authenticate(self, username: str, password: str):
        user = self.repo.get_by_username(username)
        if not user:
            return None
        
        if pwd_context.verify(password, user.hashed_password):
            return user
        return None