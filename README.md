# Jedha_ETL_Kayak

Projet ETL : Kayak

## Structure des dossiers

Les sources sont organisées de la manière suivante :

* **scripts/** :
  * **01_get_coordinates.py** : récupération des coordonnées des villes françaises
  * **02_get_weather_data.py** : collecte des données météo via API OpenWeatherMap
  * **03_booking_scraper.py** : script de scraping Booking.com
  * **04_scrape_all_cities.py** : orchestration du scraping pour toutes les villes
  * **05_merge_all_hotels.py** : fusion de tous les datasets d hôtels
  * **06_upload_s3.py** : upload des données vers AWS S3
  * **07_ETL_clean.py** : nettoyage et transformation des données + stockage PostgreSQL
  * **08_plotly_maps_2.py** : génération des cartes interactives Plotly

* **data/** : contient les fichiers CSV et JSON collectés avec les données météo et hôtels

* **outputs/** : contient les cartes interactives HTML générées (top 5 destinations et top 20 hôtels)

## Prérequis

* python 3.12+
* avoir les comptes suivants :
  * API OpenWeatherMap : créer un compte gratuit sur leur site
  * AWS : créer un bucket S3 et une database PostgreSQL

* un fichier `.env` qui contient les clés suivantes :
  * WEATHER_KEY="YOUR_OPENWEATHERMAP_API_KEY"
  * AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
  * AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
  * PWD_DB="YOUR_POSTGRESQL_PASSWORD"
