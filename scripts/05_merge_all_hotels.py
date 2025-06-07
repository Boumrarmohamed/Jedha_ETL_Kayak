import pandas as pd
import json

df_weather = pd.read_csv("data/weather_data.csv")
df_cities = pd.read_csv("data/coordonnees_villes.csv")
df_hotels = pd.DataFrame(json.load(open('data/all_hotels.json', 'r', encoding='utf-8')))

# Nettoyer hôtels
import html
df_hotels[['latitude', 'longitude', 'score']] = df_hotels[['latitude', 'longitude', 'score']].apply(pd.to_numeric, errors='coerce')
df_hotels['name'] = df_hotels['name'].apply(lambda x: html.unescape(str(x)))
df_hotels['description'] = df_hotels['description'].apply(lambda x: html.unescape(str(x)))

# Merger tout
df_final = pd.merge(pd.merge(df_weather, df_cities, on='city_name'), df_hotels, on='city_name')

# Nettoyer colonnes dupliquées
for col in ['latitude', 'longitude', 'city_id']:
    if f'{col}_x' in df_final.columns:
        df_final[col] = df_final[f'{col}_x']
        df_final = df_final.drop([f'{col}_x', f'{col}_y'], axis=1)

# Nettoyer descriptions
if 'description_x' in df_final.columns and 'description_y' in df_final.columns:
    df_final['description'] = df_final['description_y']
    df_final = df_final.drop(['description_x', 'description_y'], axis=1)

# Sauvegarder
df_final.to_csv('data/35Cities_Weather_Hotels_FINAL.csv', index=False)
df_final.to_json('data/35Cities_Weather_Hotels_FINAL.json', orient='records', indent=2)
print(f"Fini ! {len(df_final)} lignes dans CSV et JSON")