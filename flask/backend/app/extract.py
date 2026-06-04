import requests
import os
import json
import logging
from dotenv import load_dotenv
from datetime import date,datetime
from models import TwCities
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
#print("Import successfully") #For checking
load_dotenv()

#===============Set up====================
logging.basicConfig(
    filename='extract.log',
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
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
            logging.error(f"Network error/ fail to call API: {net_err}")
            continue
    if all_cities_weather:    
        with open('all_cities_weather.json', mode='w', encoding='utf-8') as file:
            json.dump(all_cities_weather, file, indent=4, ensure_ascii=False)
            logging.info(f'file is successfully written {len(all_cities_weather)} cities')
    else:
        logging.info('No record was written')
except Exception as e:
    logging.error(f'Error: {e}')
finally:
    session.close()