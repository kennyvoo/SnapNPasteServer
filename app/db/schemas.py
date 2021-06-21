from fastapi_users import models
from pydantic import UUID4, BaseModel
import uuid
from typing import List, Optional


###History
class HistoryBase(BaseModel):
    text: str


class HistoryCreate(HistoryBase):
    pass


class History(HistoryBase):
    id: int
    owner_email: str

    class Config:
        orm_mode = True

#User

class User(models.BaseUser):
    username : str

class UserCreate(models.BaseUserCreate):
    username : str


class UserUpdate(User, models.BaseUserUpdate):
    username: str

# added del user_dict['history'] at sqlalchemy line 154 to make it

class UserDB(User, models.BaseUserDB):
    username : str
    history : List[History] = []


    class Config:
        orm_mode = True


###History
class FeedbackBase(BaseModel):
    text: str
    user_email : str


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int
    user_email : str

    class Config:
        orm_mode = True