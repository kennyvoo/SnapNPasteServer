from fastapi_users import models
from pydantic import UUID4, BaseModel
import uuid

class User(models.BaseUser):
    username : str


class UserCreate(models.BaseUserCreate):
    username : str


class UserUpdate(User, models.BaseUserUpdate):
    username: str


class UserDB(User, models.BaseUserDB):
    username : str

class feedback(BaseModel):
    id: UUID4
    feedback: str
    class Config:
        orm_mode = True