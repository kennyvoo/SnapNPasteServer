from .db_init import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    owner_email = Column(String, ForeignKey("user.email"))
    owner = relationship("UserTable", back_populates="history")

class UserTable(Base, SQLAlchemyBaseUserTable):
    username = Column(String(length=32), nullable=False)
    history = relationship("History", back_populates="owner")

