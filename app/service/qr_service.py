from datetime import datetime, timedelta
import uuid
from app.repository.qr_repository import QRRepository

class QRService:
    def __init__(self, repo: QRRepository):
        self.repo = repo

    def generate_qr(self, user_id: int):
        code = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=5)

        return self.repo.create(
            code=code,
            expires_at=expires_at,
            user_id=user_id
        )

    def confirm_qr(self, code: str):
        print(f"[DEBUG] Trying to confirm code: {code}")  # ← добавили
        
        qr = self.repo.get_by_code(code)
        
        if not qr:
            print("[DEBUG] QR not found in database")
            return None

        print(f"[DEBUG] Found QR: user_id={qr.user_id}, is_used={qr.is_used}, expires_at={qr.expires_at}")

        if qr.is_used:
            print("[DEBUG] QR already used")
            return None

        if qr.expires_at < datetime.utcnow():
            print("[DEBUG] QR expired")
            return None

        self.repo.mark_as_used(qr)
        print("[DEBUG] QR confirmed successfully")
        
        return qr