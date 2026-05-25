from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import DataCreate, DataResponse
from app.service.data_service import DataService
from app.repository.data_repository import DataRepository

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/", response_model=DataResponse)
def create_data(
    request: Request,  
    data: DataCreate, 
    db: Session = Depends(get_db)
):
    
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized"
        )

    repo = DataRepository(db)
    service = DataService(repo)
    return service.create_data(data.text, user_id)


@router.get("/")
def get_my_data(
    request: Request,  # Добавляем request
    db: Session = Depends(get_db)
):
    
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized"
        )

    repo = DataRepository(db)
    service = DataService(repo)
    data_list = service.get_user_data(user_id)
    return data_list
