from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from redis import Redis

redis_client = Redis(host="127.0.0.1", port=6379)
BASE_DIR = Path(__file__).resolve().parent


class DBConnect(BaseModel):
    url_db: str = "postgresql+asyncpg://root:root@localhost:5433/authorization_db"
    echo: bool = True
    expire_on_commit: bool = False
    autocommit: bool = False
    autoflush: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class CookiesAuth(BaseModel):
    cookie_key: str = "auth-app-session"


class UrlAPI(BaseModel):
    check_auth: str = "http://0.0.0.0:8000/auth/check_auth_token"
    login_user: str = "http://0.0.0.0:8000/auth/login"


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    url_api: UrlAPI = UrlAPI()
    cookie_auth: CookiesAuth = CookiesAuth()
    db_settings: DBConnect = DBConnect()


settings = Settings()