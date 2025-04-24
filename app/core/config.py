from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Terminal Recommender System"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # AI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    LOCAL_LLM_ENABLED: bool = os.getenv("LOCAL_LLM_ENABLED", "false").lower() == "true"
    
    # M-Pesa Configuration
    MPESA_CONSUMER_KEY: str = os.getenv("MPESA_CONSUMER_KEY", "")
    MPESA_CONSUMER_SECRET: str = os.getenv("MPESA_CONSUMER_SECRET", "")
    MPESA_ENV: str = os.getenv("MPESA_ENV", "sandbox")
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Frontend development
        "http://localhost:5173",  # Vite development server
        "https://lovable-ai.vercel.app",  # Lovable AI production
        "https://lovable-ai.netlify.app",  # Lovable AI production (Netlify)
        "https://your-production-domain.com"  # Production frontend
    ]
    
    # Product API Keys
    JUMIA_API_KEY: Optional[str] = os.getenv("JUMIA_API_KEY")
    AMAZON_API_KEY: Optional[str] = os.getenv("AMAZON_API_KEY")
    
    # Sentry Configuration
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 