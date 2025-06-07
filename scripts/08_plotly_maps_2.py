import pandas as pd
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

# Prendre une ligne par ville
df_villes = df.groupby('city_name').first().reset_index()

# Sélectionner les 5 villes les plus chaudes
top5_destinations = df_villes.nlargest(5, 'temp')

print("Top-5 destinations:")
print(top5_destinations[['city_name', 'temp']])

# Carte des top-5 destinations
fig1 = px.scatter_mapbox(top5_destinations, 
                        lat="latitude", 
                        lon="longitude", 
                        color="temp",
                        size="temp",
                        hover_name="city_name",
                        hover_data=["temp", "humidity", "wind"],
                        mapbox_style="carto-positron",
                        zoom=5,
                        width=700, 
                        height=600,
                        title="Top-5 destinations météo en France")

fig1.show()

# CARTE 2: TOP-20 HÔTELS
df_hotels = df.groupby('name').first().reset_index()

# Sélectionner les 20 hôtels avec les meilleurs scores
top20_hotels = df_hotels.nlargest(20, 'score')

print("Top-20 hôtels:")
print(top20_hotels[['name', 'city_name', 'score']])

# Carte des top-20 hôtels
fig2 = px.scatter_mapbox(top20_hotels, 
                        lat="latitude", 
                        lon="longitude", 
                        color="score",
                        size="score",
                        hover_name="name",
                        hover_data=["city_name", "score"],
                        mapbox_style="carto-positron",
                        zoom=4.5,
                        center={"lat": 46.5, "lon": 2.0},
                        width=700, 
                        height=600,
                        title="Top-20 hôtels en France")

fig2.show()

# Export HTML pour garder l'interactivité
fig1.write_html("outputs/top5_destinations.html")
fig2.write_html("outputs/top20_hotels.html")

print("Cartes exportées en HTML (interactives) !")
print("Ouvrez les fichiers .html dans votre navigateur")
