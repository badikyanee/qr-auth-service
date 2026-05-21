from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
class QRLoginData(BaseModel):
    code: str

class DataCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)

class DataResponse(BaseModel):
    id: int
    text: str
    user_id: int

class DataCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)

class DataResponse(BaseModel):
    id: int
    text: str
    user_id: int

    class Config:
        from_attributes = True