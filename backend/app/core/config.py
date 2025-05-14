from typing import List, Optional
from pydantic import BaseSettings, validator, EmailStr, AnyHttpUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "Leymax POS System"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "A multi-company POS system for bakery, tools shop, and academy"
    API_V1_STR: str = "/api/v1"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]  # Frontend URL
    
    # Database Settings
    DATABASE_URL: str = "mysql://root:@localhost/leymax_webpos"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Pusher Settings
    PUSHER_APP_ID: str = ""
    PUSHER_KEY: str = ""
    PUSHER_SECRET: str = ""
    PUSHER_CLUSTER: str = "ap2"
    
    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = ""
    SMTP_USER: Optional[str] = ""
    SMTP_PASSWORD: Optional[str] = ""
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
