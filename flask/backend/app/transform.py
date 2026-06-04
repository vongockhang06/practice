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
    temp_df = df.drop(columns=['timezone','timezone_offset','prev','next','lat','lon'])
    ls=[]
    for i in range(len(temp_df)):#per city   
        row=temp_df.iloc[i]
        data=row['data']
        city=row['city_name']
        for j in range(len(data)): #per day
            day_data=data[j]
            timestamp=day_data['dt']
            date_time_obj = datetime.fromtimestamp(timestamp)
    
        #Extract necessary info
            forecast_date =date_time_obj.date()
            temp2=day_data['temp']
        
            temp_day=temp2['day']
            temp_min=temp2['min']
            temp_max=temp2['max']
            
            pressure=day_data['pressure']
            humidity=day_data['humidity']
            raw_rain = day_data.get('rain', 0.0)
            if isinstance(raw_rain, dict):
                # Nếu rain có dạng {"1h": 1.5}, câu lệnh dưới đây sẽ bóc tách ra con số 1.5
                rain_volume = float(list(raw_rain.values())[0])
            else:
                rain_volume = float(raw_rain)
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
