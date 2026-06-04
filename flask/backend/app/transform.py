from datetime import datetime,date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import json
import logging
from dotenv import load_dotenv
import os
from models import TwCities,WeatherDailyForecasts
#========================================
load_dotenv()
USER_NAME=os.getenv('USER_NAME')
DB_PASSWORD=os.getenv('DB_PASSWORD')
engine=create_engine(f'postgresql+psycopg2://{USER_NAME}:{DB_PASSWORD}@localhost:5432/tw_weather_db')
Session =sessionmaker(bind=engine)
session = Session()
#========================================
logging.basicConfig(
    filename='transform.log',
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

try:
    file_name='all_cities_weather.json'
    df= pd.read_json(file_name)
    temp_df = df.drop(columns=['timezone','timezone_offset','prev','next'])
    lat_val = float(temp_df['lat'].iloc[0])
    lon_val = float(temp_df['lon'].iloc[0])
    city = session.query(TwCities.city_name)\
                  .filter(TwCities.latitude == round(lat_val, 4), 
                          TwCities.longitude == round(lon_val, 4))\
                  .scalar()
    temp_df = temp_df.drop(columns=['lat','lon'])
    temp_df['city']=city
    ls=[]
    for i in range(len(temp_df)):   
        row=temp_df.iloc[i]
        data=row['data']
        timestamp=data['dt']
        date_time_obj = datetime.fromtimestamp(timestamp)
    
        #Extract necessary info
        forecast_date =date_time_obj.date()
        city=row['city']
        temp = row['data']
        temp2=temp['temp']
        
        temp_day=temp2['day']
        temp_min=temp2['min']
        temp_max=temp2['max']
        
        pressure=temp['pressure']
        humidity=temp['humidity']
        rain_volume=temp.get('rain',0.0)
        temp_list=[forecast_date,city,temp_day,temp_min,temp_max,pressure,humidity,rain_volume]
        ls.append(temp_list)
        
    cols=['forecast_date','city_name','temp_day','temp_min',
          'temp_max','pressure','humidity','rain_volume']    
    new_df=pd.DataFrame(ls,columns=cols)
    new_df['forecast_date'] = new_df['forecast_date'].astype(str)
except Exception as e:
    session.rollback()
    logging.error(f"\nError message: {e}")
finally:
    session.close()
    
try:
    new_df.to_json('cleaned_weather.json', orient='records', 
                   date_format='iso', indent=4, force_ascii=False)
    logging.info('write file successfully')
except:
    logging.error('Cannot write file')
