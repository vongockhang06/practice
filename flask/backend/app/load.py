import logging
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from models import WeatherDailyForecasts
from dotenv import load_dotenv
import os

load_dotenv()
USER_NAME=os.getenv('USER_NAME')
DB_PASSWORD=os.getenv('DB_PASSWORD')
engine=create_engine(f'postgresql+psycopg2://{USER_NAME}:{DB_PASSWORD}@localhost:5432/tw_weather_db')
Session=sessionmaker(bind=engine)
session=Session()
logging.basicConfig(
    filename='load.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


try:
    df = pd.read_json('cleaned_weather.json')
    records = df.to_dict(orient='records')
    
    if records:
        stmt = insert(WeatherDailyForecasts)
        
        upsert_stmt = stmt.on_conflict_do_update(

            constraint='unique_location_date',             
            set_={
                'temp_day': stmt.excluded.temp_day,
                'temp_min': stmt.excluded.temp_min,
                'temp_max': stmt.excluded.temp_max,
                'pressure': stmt.excluded.pressure,
                'humidity': stmt.excluded.humidity,
                'rain_volume': stmt.excluded.rain_volume
            }
        )
        session.execute(upsert_stmt, records)
        session.commit()
    logging.info('Loading into database successfully')
except Exception as e:
    session.rollback()
    logging.error(f'Error: {e}')
finally:
    session.close()