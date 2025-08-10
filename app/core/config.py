from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Snapped AI"
    
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    MAX_SIMILAR_PRODUCTS: int = int(os.getenv("MAX_SIMILAR_PRODUCTS", "30"))
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Upload settings
    UPLOAD_FOLDER: str = "app/static/uploads"
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg", "gif"}
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "12000"))

settings = Settings()