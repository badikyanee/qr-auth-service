from sqlalchemy.orm import Session
from datetime import datetime
from app.models.qr_session import QRSession

class QRRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, code: str, expires_at: datetime, user_id: int):
        qr = QRSession(
            code=code,
            expires_at=expires_at,
            user_id=user_id,
            is_used=False,
            is_confirmed=False
        )
        self.db.add(qr)
        self.db.commit()
        self.db.refresh(qr)
        return qr

    def get_by_code(self, code: str):
        return self.db.query(QRSession).filter(QRSession.code == code).first()

    def mark_as_used(self, qr: QRSession):
        # Перезагружаем объект в текущей сессии, чтобы избежать detached instance
        qr = self.db.merge(qr)
        qr.is_used = True
        self.db.commit()
        self.db.refresh(qr)
        return qr