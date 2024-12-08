import os

class Config:
    APP_NAME = "Chat Application"
    VERSION = "1.0.0"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    UPLOAD_DIR = "uploads/"
