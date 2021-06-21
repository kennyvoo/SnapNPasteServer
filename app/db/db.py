from .db_init import SessionLocal, engine,database
from . import crud, models, schemas
from fastapi_users.db import  SQLAlchemyUserDatabase

#Base.metadata.create_all(engine)
models.Base.metadata.create_all(bind=engine)

users = models.UserTable.__table__
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_db = SQLAlchemyUserDatabase(schemas.UserDB, database, users)

