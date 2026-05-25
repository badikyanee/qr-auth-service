from fastapi import FastAPI

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

from app.models import user 

from app.api.auth import router as auth_router
from app.api.qr import router as qr_router
from app.api.data import router as data_router


from app.core.middleware import AuthMiddleware


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="QR Authentication Backend (FastAPI + PostgreSQL + JWT)",
    version="1.0.0",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True
    }
)



app.add_middleware(AuthMiddleware)



Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(qr_router)
app.include_router(data_router)


@app.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "status": "running",
        "docs": "/docs"
    }
