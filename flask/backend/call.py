import requests
import os
import json
from dotenv import load_dotenv
from datetime import date,datetime
#print("Import successfully") #For checking


load_dotenv()
#===============Location of taichung=======================


#===============Set up====================
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

response=requests.get(url=url,params=params)
data=response.json()
print(data)