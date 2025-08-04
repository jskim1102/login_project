# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# BaseSettings를 상속받은 Settings 클래스의 인스턴스가 생성될 때 .env 파일의 정보를 읽어옴
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # .env 파일의 경로 설정
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

@lru_cache() # 설정 객체를 캐싱하여 반복 로드를 방지하는 데코레이터
def get_settings() -> Settings:
    return Settings()

# BaseSettings를 상속받은 Settings 클래스의 인스턴스가 생성될 때 .env 파일의 정보를 읽어옴
settings = get_settings()