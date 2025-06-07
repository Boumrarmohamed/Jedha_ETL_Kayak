import pandas as pd
import re

print("Analyse complète du fichier CSV")
print("="*50)

# Charger le fichier
df = pd.read_csv('35Cities_Weather_Hotels_FINAL.csv')
print(f"Total lignes: {len(df)}")
print(f"Total colonnes: {len(df.columns)}")

print("\n1. PROBLÈMES DANS LES NOMS D'HÔTELS:")
print("-" * 30)
# Chercher des caractères suspects dans les noms
noms_suspects = df[df['name'].str.contains(r'[<>&"\\]', na=False, regex=True)]
if len(noms_suspects) > 0:
    print(f"Noms avec caractères suspects: {len(noms_suspects)}")
    print(noms_suspects['name'].head(10).tolist())
else:
    print("Aucun caractère suspect dans les noms")

print("\n2. PROBLÈMES DANS LES DESCRIPTIONS:")
print("-" * 30)
# Chercher des balises HTML
html_descriptions = df[df['description'].str.contains(r'<[^>]*>', na=False, regex=True)]
print(f"Descriptions avec balises HTML: {len(html_descriptions)}")

# Chercher des guillemets doubles
double_quotes = df[df['description'].str.contains(r'""', na=False, regex=True)]
print(f"Descriptions avec guillemets doubles: {len(double_quotes)}")

# Chercher des descriptions coupées (se terminant par un mot incomplet)
descriptions_coupees = df[df['description'].str.endswith((' à resp', ' à', ' de', ' le', ' la', ' du', ' des'), na=False)]
print(f"Descriptions probablement coupées: {len(descriptions_coupees)}")

print("\n3. PROBLÈMES DANS LES URLS:")
print("-" * 30)
# URLs trop longues
urls_longues = df[df['url'].str.len() > 500]
print(f"URLs très longues (>500 caractères): {len(urls_longues)}")

# URLs cassées
urls_cassees = df[~df['url'].str.startswith('https://', na=False)]
print(f"URLs qui ne commencent pas par https://: {len(urls_cassees)}")

print("\n4. VALEURS MANQUANTES PAR COLONNE:")
print("-" * 30)
for col in df.columns:
    missing = df[col].isnull().sum()
    if missing > 0:
        print(f"{col}: {missing} valeurs manquantes")

print("\n5. VALEURS ABERRANTES:")
print("-" * 30)
# Scores aberrants
scores_aberrants = df[(df['score'] < 0) | (df['score'] > 10)]
print(f"Scores aberrants (<0 ou >10): {len(scores_aberrants)}")

# Températures aberrantes
temp_aberrantes = df[(df['temp'] < -50) | (df['temp'] > 60)]
print(f"Températures aberrantes: {len(temp_aberrantes)}")

print("\n6. DOUBLONS:")
print("-" * 30)
doublons = df.duplicated().sum()
print(f"Lignes exactement identiques: {doublons}")

# Doublons partiels (même hôtel, même ville, même date)
doublons_partiels = df.duplicated(subset=['city_name', 'name', 'date']).sum()
print(f"Doublons hôtel/ville/date: {doublons_partiels}")

print("\n7. ÉCHANTILLON DE PROBLÈMES:")
print("-" * 30)
if len(html_descriptions) > 0:
    print("Exemple de description avec HTML:")
    print(html_descriptions['description'].iloc[0][:200] + "...")

print("\n8. CARACTÈRES SPÉCIAUX FRÉQUENTS:")
print("-" * 30)
# Analyser tous les caractères spéciaux dans les descriptions
all_descriptions = ' '.join(df['description'].dropna())
caracteres_speciaux = re.findall(r'[^\w\s\-.,;:!?()\'\"/]', all_descriptions)
from collections import Counter
top_caracteres = Counter(caracteres_speciaux).most_common(10)
for char, count in top_caracteres:
    print(f"'{char}': {count} occurrences")

print("\n" + "="*50)
print("Analyse terminée")