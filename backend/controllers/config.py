import os

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)
# ======================================
# MAIN CONFIG CLASS
# ======================================

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "placement-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwt-secret-key"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 300
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "guptayush30@gmail.com"
    MAIL_PASSWORD = "@yusH"
    MAIL_DEFAULT_SENDER = "guptayush30@gmail.com"

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = [
        "pdf",
        "doc",
        "docx"
    ]
class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///placement_portal.sqlite3"
    )
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///placement_portal.sqlite3"
    )