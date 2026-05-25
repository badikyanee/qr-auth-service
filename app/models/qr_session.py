from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.db.base import Base

class QRSession(Base):
    __tablename__ = "qr_sessions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    is_confirmed = Column(Boolean, default=False)
    is_used = Column(Boolean, default=False)          # ← добавили
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<QRSession {self.code}>"