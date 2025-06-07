import os
import pandas as pd
import json

df_weather = pd.read_csv("data/weather_data.csv")
top_35_France = df_weather['city_name'].unique().tolist()  

print(f"{len(top_35_France)} villes trouvees")

# Lancer le scraping pour chacune des 35 villes
for ville in top_35_France:
    print(f"Scraping {ville}...")
    os.system(f'python scripts/03_booking_scraper.py "{ville}"')

print("Scraping termine !")
print("Combinaison des fichiers...")

all_hotels = []

for ville in top_35_France:
    filename = f"data/result_booking_{ville}.json"
    
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            hotels = json.load(f)
        
        # Ajouter le nom de ville à chaque hôtel
        for hotel in hotels:
            hotel['city_name'] = ville
        
        all_hotels.extend(hotels)
        print(f"  {ville}: {len(hotels)} hotels")
    else:
        print(f"  {ville}: fichier manquant")

# Sauvegarder tout en un fichier
with open('data/all_hotels.json', 'w', encoding='utf-8') as f:
    json.dump(all_hotels, f, ensure_ascii=False, indent=2)

print(f"Termine ! {len(all_hotels)} hotels dans all_hotels.json")