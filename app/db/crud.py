from sqlalchemy.orm import Session

from . import models, schemas

# History
def get_history(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.History).offset(skip).limit(limit).all()

def create_user_history(db: Session, item: schemas.HistoryCreate, user_email: str):
    db_item = models.History(**item.dict(), owner_email=user_email)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_history(db: Session, user_email: str):
    return db.query(models.UserTable).filter(models.UserTable.email == user_email).first().history

def delete_all_history(db: Session, user_email: str):
    history=db.query(models.History).filter(models.History.owner_email == user_email).delete()
    db.commit()
    return "successful"

# Feedback

def get_all_feedback(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feedback).offset(skip).limit(limit).all()

def create_feedback(db: Session, item: schemas.FeedbackCreate, user_email: str):
    db_item = models.Feedback(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item