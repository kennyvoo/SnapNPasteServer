from fastapi_users import FastAPIUsers
from core.security import jwt_authentication 
from db.db import user_db
from db.schemas import *

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)