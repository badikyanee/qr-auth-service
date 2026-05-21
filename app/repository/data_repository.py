from sqlalchemy.orm import Session
from app.models.data import Data

class DataRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, text: str, user_id: int) -> Data:
        data = Data(text=text, user_id=user_id)
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def get_by_user(self, user_id: int):
        return self.db.query(Data).filter(Data.user_id == user_id).all()