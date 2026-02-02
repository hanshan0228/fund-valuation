from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "基金估值系统"
    DEBUG: bool = True

    # 数据库
    DATABASE_URL: str = "sqlite:///./data/database.db"

    # OCR
    OCR_USE_GPU: bool = False
    OCR_LANG: str = "ch"

    # 基金API
    FUND_API_TIMEOUT: int = 10
    FUND_CACHE_TTL: int = 300

    # 定时任务
    ENABLE_SCHEDULER: bool = True
    UPDATE_INTERVAL: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
