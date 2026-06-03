import requests
import os
import json
import logging
from dotenv import load_dotenv
from datetime import date,datetime
#print("Import successfully") #For checking
load_dotenv()

#===============Set up====================
logging.basicConfig(
    filename='data.log',
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

API_KEY=os.getenv("API_KEY")
#print(API_KEY) #For checking
url = "https://api.openweathermap.org/data/4.0/onecall/timeline/1day"
params={
    'lon': 120.736,
    'lat': 24.147736,
    'appid':API_KEY,
    'units': 'metric',
    'lang': 'en'
}
#Reading API documentation for more details
try:
    response=requests.get(url=url,params=params)
    response.raise_for_status()
    data=response.json()
    with open('taichung_weather.json',mode='w') as file:
        json.dump(data,file,indent=4,ensure_ascii=False)
        logging.info(f'file is successfully written')
except requests.exceptions.RequestException as net_err:
    logging.error(f"Network error/ fail to call API: {net_err}")
except Exception as e:
    logging.error(f"Error: {e}")