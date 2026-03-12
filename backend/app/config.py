import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/t3g_seguridad')
    MONGODB_DB = os.getenv('MONGODB_DB', 't3g_seguridad')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-key-change-in-production')
    
    # Email
    DEMO_EMAIL_DESTINO = os.getenv('DEMO_EMAIL_DESTINO', 'lalorzo450@gmail.com')