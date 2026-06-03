from datetime import datetime,date
import pandas as pd
from models import TwCities,WeatherDailyForecasts
file_name='taichung_weather.json'
df= pd.read_json(file_name)
temp_df = df.drop(columns=['timezone','timezone_offset'])
print(temp_df)