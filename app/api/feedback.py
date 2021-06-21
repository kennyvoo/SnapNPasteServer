from typing import List

from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter
from core.fastapi_user_auth import fastapi_users

from db import crud, models, schemas
from db.db import SessionLocal,get_db


router = APIRouter()


@router.post("/users/{user_email}/feedback")
def create_feedback(
    user_email: str, item: schemas.FeedbackCreate, db: Session = Depends(get_db),User= Depends(fastapi_users.current_user())):
    return crud.create_feedback(db=db, item=item, user_email=user_email)


@router.get("/all_feedback", response_model=List[schemas.Feedback])
def get_all_feedback(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),User= Depends(fastapi_users.current_user())):
    items = crud.get_all_feedback(db, skip=skip, limit=limit)
    return items
