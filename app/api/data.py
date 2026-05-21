from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import DataCreate, DataResponse
from app.service.data_service import DataService
from app.repository.data_repository import DataRepository
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/", response_model=DataResponse)
def create_data(
    data: DataCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = DataRepository(db)
    service = DataService(repo)
    return service.create_data(data.text, current_user.id)


@router.get("/")
def get_my_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = DataRepository(db)
    service = DataService(repo)
    data_list = service.get_user_data(current_user.id)
    return data_list