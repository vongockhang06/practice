import requests
import json
from datetime import date,datetime
from models import TwCities
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
from utils import setup_pipeline_logging
#print("Import successfully") #For checking


#===============Set up====================
logger=setup_pipeline_logging()
url = get_url_1day()
session=get_db_session()
API_KEY=get_API_KEY()
try:
    cities=session.query(TwCities).all()
    all_cities_weather=[]
    for city in cities:
        params={
        'lon': city.longitude,
        'lat': city.latitude,
        'appid':API_KEY,
        'units': 'metric',
        'lang': 'en'
        }
        #Reading API documentation for more details
        try:
            response=requests.get(url=url,params=params)
            response.raise_for_status()
            data=response.json()
            data['city_name'] = city.city_name
            all_cities_weather.append(data)
        except requests.exceptions.RequestException as net_err:
            logger.error(f"Network error/ fail to call API: {net_err}")
            continue
    if all_cities_weather:    
        with open('all_cities_weather.json', mode='w', encoding='utf-8') as file:
            json.dump(all_cities_weather, file, indent=4, ensure_ascii=False)
            logger.info(f'file is successfully written {len(all_cities_weather)} cities')
    else:
        logger.info('No record was written')
except Exception as e:
    logger.error(f'Error: {e}')
finally:
    session.close()