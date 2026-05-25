from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.qr_session import QRSession
from app.models.data import Data

Base.metadata.create_all(bind=engine)

print("Tables created")