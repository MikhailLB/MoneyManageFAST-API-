from pathlib import Path
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000

class ApiPrefix(BaseModel):
    prefix: str = "/api/v1"

class DataBaseConfig(BaseSettings):
    url: str = PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

class AuthJWT(BaseModel):
    private_key: Path = BASE_DIR / 'certs' / 'private.pem'
    public_key: Path = BASE_DIR / 'certs' / 'public.pem'
    algorithm: str = 'RS256'
    expire_minutes: int = 15
    refresh_token_expire_days: int = 7


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DataBaseConfig
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()
