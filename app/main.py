from fastapi import FastAPI
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.qr import router as qr_router
from app.api.data import router as data_router



app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG
)

app.include_router(auth_router)
app.include_router(qr_router)
app.include_router(data_router)

@app.get("/")
async def root():
    return {
        "message": "QR Auth Backend is running! ✅",
        "docs": "/docs"
    }