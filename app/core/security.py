from fastapi_users.authentication import JWTAuthentication
from core import Config



jwt_authentication = JWTAuthentication(secret= Config.SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")

