import databases
import sqlalchemy
from fastapi import FastAPI
from fastapi_users import models
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import  Column, String
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

#Base: DeclarativeMeta = declarative_base()
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



