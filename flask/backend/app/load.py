import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from models import WeatherDailyForecasts
from config import get_db_session
from utils import setup_pipeline_logging
session=get_db_session()
logger=setup_pipeline_logging()
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
    logger.info('Loading into database successfully')
except Exception as e:
    session.rollback()
    logger.error(f'Error: {e}')
finally:
    session.close()