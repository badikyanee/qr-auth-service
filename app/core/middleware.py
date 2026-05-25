import jwt
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Защищаем только эндпоинты, которые начинаются с /data
        if request.url.path.startswith("/data"):
            auth_header = request.headers.get("Authorization")
            
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Missing or invalid credentials"}
                )
            
            try:
                token = auth_header.split(" ")[1]
                # Декодируем JWT
                payload = jwt.decode(
                    token, 
                    settings.SECRET_KEY, 
                    algorithms=[settings.ALGORITHM]
                )
                user_id = payload.get("sub")
                if user_id is None:
                    raise jwt.PyJWTError()
                
                # Приводим к инту, так как в auth.py мы теперь строго пишем str(user.id)
                request.state.user_id = int(user_id)
                
            except (jwt.PyJWTError, IndexError, ValueError):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Could not validate credentials"}
                )

        response = await call_next(request)
        return response
