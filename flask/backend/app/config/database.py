# config/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables once here
load_dotenv()

USER_NAME = os.getenv('USER_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
API_KEY = os.getenv("API_KEY")  # Keeping API key accessible here as well

# Production fallback logic: default to localhost port if env isn't set
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'tw_weather_db')

DATABASE_URL = f'postgresql+psycopg2://{USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create a single engine instance
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)
url1day="https://api.openweathermap.org/data/4.0/onecall/timeline/1day"
url15m='https://api.openweathermap.org/data/4.0/onecall/timeline/15min'
url1m='https://api.openweathermap.org/data/4.0/onecall/timeline/1min'
def get_db_session():
    """Provides a transactional database session context."""
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.rollback()
        raise
def get_API_KEY():
    return API_KEY
def get_url_1day():
    return url1day