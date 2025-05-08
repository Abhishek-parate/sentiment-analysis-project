import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///db/db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Groq API key
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')