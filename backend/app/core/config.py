from typing import List, Optional
from pydantic import validator, EmailStr, AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Leymax POS System"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "A multi-company POS system for bakery, tools shop, and academy"
    API_V1_STR: str = "/api/v1"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React default
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1"
    ]
    
    # Database Settings - XAMPP MySQL default configuration
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/leymax_webpos"
    
    # Security Settings
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
