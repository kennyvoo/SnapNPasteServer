from fastapi_users import FastAPIUsers
from fastapi import  Request,APIRouter
from core.security import jwt_authentication 
from db.db import user_db
from db.base_class import *
from core.Config import SECRET

def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


router = APIRouter()

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt"
)
router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth"
)
router.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
)
router.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
)
router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


