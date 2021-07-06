from typing import List

from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter
from core.fastapi_user_auth import fastapi_users

from db import crud, models, schemas
from db.db import SessionLocal,get_db


router = APIRouter()


@router.post("/users/{user_email}/history")
def create_item_for_user(
    user_email: str, item: schemas.HistoryCreate, db: Session = Depends(get_db),User= Depends(fastapi_users.current_user())):
    return crud.create_user_history(db=db, item=item, user_email=user_email)


@router.get("/all_history", response_model=List[schemas.History])
def get_all_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),User= Depends(fastapi_users.current_user())):
    items = crud.get_history(db, skip=skip, limit=limit)
    return items

@router.get("/history/{user_email}", response_model=List[schemas.History])
def read_user_history(user_email:str, db: Session = Depends(get_db),User= Depends(fastapi_users.current_user())):
    items = crud.get_user_history(db, user_email=user_email)
    return items

@router.delete("/history/{user_email}/delete_all")
def delete_user_history(user_email:str, db: Session = Depends(get_db),User= Depends(fastapi_users.current_user())):
    return crud.delete_all_history(db, user_email=user_email)


