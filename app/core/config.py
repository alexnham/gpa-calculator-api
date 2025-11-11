import os

class Config:
    """Application configuration settings."""
    
    APP_NAME = os.getenv("APP_NAME", "GPA API")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
    PDF_UPLOAD_PATH = os.getenv("PDF_UPLOAD_PATH", "uploads/")
    MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))  # 10 MB
    ALLOWED_EXTENSIONS = {'pdf'}
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Export a settings instance for `from app.core.config import settings`
settings = Config()