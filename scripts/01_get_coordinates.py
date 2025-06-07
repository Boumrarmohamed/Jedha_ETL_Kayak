import pandas as pd
import requests
from cities_data import top_35_France

# Récupération des coordonnées
Info_Cities = pd.DataFrame(columns=['city_name', 'city_id', 'latitude', 'longitude'])

header = {'User-Agent': 'ProjetKayak-CDSD'}
for i in range(len(top_35_France)):
    payload = {'q': top_35_France[i] + ', France', 'format': 'json'}
    r = requests.get(url="https://nominatim.openstreetmap.org/search?", params=payload, headers=header)
    Info_Cities.loc[i] = [top_35_France[i], i+1, r.json()[0]['lat'], r.json()[0]['lon']]

print(Info_Cities.head())

# Sauvegarde en CSV et JSON
Info_Cities.to_csv('data/coordonnees_villes.csv', index=False)
Info_Cities.to_json('data/coordonnees_villes.json', orient='records', indent=2)
print(Info_Cities.shape)