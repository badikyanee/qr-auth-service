from sqlalchemy.orm import Session
from datetime import datetime
from app.models.qr_session import QRSession

class QRRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, code: str, expires_at: datetime, user_id: int):
        # Используем правильное имя модели QRSession, которое вы импортировали
        db_qr = QRSession(
            code=code, 
            expires_at=expires_at, 
            user_id=user_id,
            is_used=False  # Явно задаем базовое состояние
        )
        self.db.add(db_qr)
        self.db.commit()      # Сохраняем запись в PostgreSQL
        self.db.refresh(db_qr) # Обновляем объект, чтобы подтянуть ID из базы
        return db_qr

    def get_by_code(self, code: str):
        return self.db.query(QRSession).filter(QRSession.code == code).first()

    def mark_as_used(self, qr: QRSession):
        # Привязываем объект к текущей сессии бэкенда
        qr = self.db.merge(qr)
        qr.is_used = True
        self.db.commit()      # Сохраняем статус "использован"
        self.db.refresh(qr)
        return qr
