import pandas as pd
import requests
from datetime import datetime, UTC
import os
from dotenv import load_dotenv
load_dotenv()
WEATHER_KEY = os.getenv("WEATHER_KEY")
from cities_data import top_35_France

# Charger les coordonnées
Info_Cities = pd.read_csv('data/coordonnees_villes.csv')

Weather_Cities = pd.DataFrame()

for id_ville in range(len(top_35_France)):
    city_name = top_35_France[id_ville]
    city_id = id_ville + 1
    
    payload = {'lat': Info_Cities.loc[id_ville, "latitude"], 
               'lon': Info_Cities.loc[id_ville, "longitude"], 
               'appid': WEATHER_KEY,
               'units': "metric",
               'exclude': 'current,minutely,hourly,alerts'
    }
    
    r = requests.get("https://api.openweathermap.org/data/3.0/onecall", params=payload)
    dict_weather = r.json()
    
    for i in range(len(dict_weather['daily'])):
        date = datetime.fromtimestamp(dict_weather['daily'][i]['dt'], UTC).strftime('%Y-%m-%d')
        temp = dict_weather['daily'][i]['temp']['day']
        temp_min = dict_weather['daily'][i]['temp']['min']
        temp_max = dict_weather['daily'][i]['temp']['max']
        humidity = dict_weather['daily'][i]['humidity']
        pressure = dict_weather['daily'][i]['pressure']
        wind = dict_weather['daily'][i]['wind_deg']
        pop = dict_weather['daily'][i]['pop'] * 100
        rain_data = dict_weather['daily'][i].get('rain', 0)
        rain = rain_data if isinstance(rain_data, (int, float)) else rain_data.get('1h', 0)
        type_weather = dict_weather['daily'][i]['weather'][0]['main']
        description = dict_weather['daily'][i]['weather'][0]['description']
        
        Weather_Cities = pd.concat([Weather_Cities, pd.DataFrame([city_name, city_id, date, temp,
                                                                  temp_min, temp_max, humidity, pressure,
                                                                  wind, pop, rain, type_weather, description]).T],
                                                                  ignore_index=True)

Weather_Cities.columns = ['city_name', 'city_id', 'date', 'temp', 'temp_min', 'temp_max',
                           'humidity', 'pressure', 'wind', 'pop', 'rain', 'type_weather', 'description']

# Analyse des meilleures destinations
city_summary = Weather_Cities.groupby(['city_name', 'city_id']).agg({
    'temp': 'mean',
    'pop': 'mean',
    'rain': 'sum'
}).reset_index()

city_summary['score'] = city_summary['temp'] - (city_summary['rain'] * 2) - (city_summary['pop'] * 0.1)
best_cities = city_summary.sort_values('score', ascending=False)

print("Top 5 destinations météo:")
print(best_cities[['city_name', 'temp', 'pop', 'rain', 'score']].head())

# Sauvegarde
Weather_Cities.to_csv('data/weather_data.csv', index=False)
best_cities.to_csv('data/best_destinations.csv', index=False)

print(Weather_Cities.shape)
