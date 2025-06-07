import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
PWD_DB = os.getenv("PWD_DB")

# Lecture des données depuis RDS
engine = create_engine(f"postgresql+psycopg2://postgres:"+PWD_DB+
                       "@database-1-kayak.cp66ow688a77.eu-west-3.rds.amazonaws.com:5432/postgres")
df = pd.read_sql("SELECT * FROM citiesweather", engine)

# CARTE 1: TOP-5 DESTINATIONS

# Calcul score météo par ville (moyenne sur toutes les dates)
weather_score = df.groupby('city_name').agg({
    'temp': 'mean',
    'humidity': 'mean', 
    'wind': 'mean',
    'pop': 'mean',
    'rain': 'mean',
    'latitude': 'first',
    'longitude': 'first'
}).reset_index()

# Score composite: temp élevée + faible humidité + faible pluie
weather_score['score_meteo'] = (weather_score['temp'] * 0.4 - 
                               weather_score['humidity'] * 0.3 - 
                               weather_score['rain'] * 0.3)

# Normaliser le score pour avoir des valeurs positives
weather_score['size_normalized'] = weather_score['score_meteo'] - weather_score['score_meteo'].min() + 1

top5_destinations = weather_score.nlargest(5, 'score_meteo')

print("Top-5 destinations:")
print(top5_destinations[['city_name', 'temp', 'score_meteo']])

# Carte TOP-5 destinations
fig1 = px.scatter_mapbox(top5_destinations, 
                        lat="latitude", 
                        lon="longitude", 
                        color="temp",
                        size="size_normalized",
                        hover_name="city_name",
                        hover_data={"temp": ":.1f", "humidity": ":.0f", "rain": ":.1f"},
                        mapbox_style="carto-positron",
                        zoom=5,
                        width=700, 
                        height=600,
                        title="Top-5 destinations météo en France",
                        color_continuous_scale="Jet")

fig1.update_traces(hovertemplate='<b>%{hovertext}</b><br>' +
                   'Température: %{customdata[0]:.1f}°C<br>' +
                   'Humidité: %{customdata[1]:.0f}%<br>' +
                   'Pluie: %{customdata[2]:.1f}mm<br>')

fig1.show()

# CARTE 2: TOP-20 HÔTELS
# Prendre une ligne par hôtel (éviter doublons dates)
hotels_unique = df.groupby(['name', 'city_name']).agg({
    'score': 'first',
    'latitude': 'first', 
    'longitude': 'first',
    'description': 'first'
}).reset_index()

# TOP-20 hôtels par score
top20_hotels = hotels_unique.nlargest(20, 'score')

print("\nTop-20 hôtels:")
print(top20_hotels[['name', 'city_name', 'score']])

# Descriptions courtes
top20_hotels = top20_hotels.copy()
top20_hotels['short_desc'] = top20_hotels['description'].str[:150] + "..."

# Carte TOP-20 hôtels
fig2 = px.scatter_mapbox(top20_hotels, 
                        lat="latitude", 
                        lon="longitude", 
                        color="score",
                        size="score",
                        hover_name="name",
                        hover_data={"city_name": True, "score": ":.1f"},
                        mapbox_style="carto-positron",
                        zoom=5,
                        width=700, 
                        height=600,
                        title="Top-20 hôtels en France",
                        color_continuous_scale="Viridis")

fig2.update_traces(hovertemplate='<b>%{hovertext}</b><br>' +
                   'Ville: %{customdata[0]}<br>' +
                   'Score: %{customdata[1]:.1f}/10<br>')

fig2.show()

# Export HTML
fig1.write_html("top5_destinations.html")
fig2.write_html("top20_hotels.html")

print("2 cartes exportées: top5_destinations.html et top20_hotels.html")
