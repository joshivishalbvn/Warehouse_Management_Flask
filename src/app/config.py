import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/whmanagement-flask'
    SECRET_KEY = os.getenv('SECRET_KEY')
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/0"  
    broker_connection_retry_on_startup = True     
    LOCAL_HOST = os.getenv('LOCAL_HOST')
    SUPER_USER = {
        "ADMIN_EMAIL": "whadmin@yopmail.com",
        "ADMIN_PASSWORD": "admin@123"
    }
