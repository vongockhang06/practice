import requests
import pandas as pd
import os
from datetime import date, datetime


def ingestion(url:str, name:str):
    time =datetime.now().strftime('%Y-%m-%d')
    output_dir = os.path.join('landing_zone',time)
    os.makedirs(output_dir,exist_ok=True)
    file_path=os.path.join(output_dir,f'{name}.csv')
    
    response=requests.get(url,timeout=10)
    response.raise_for_status()
    with open(file_path,mode='wb') as f:
        f.write(response.content)
    return file_path

url='https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
name=ingestion(url,'titanic')
df=pd.read_csv(name)
print(df.head(5))    