import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
PWD_DB = os.getenv("PWD_DB")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Extract
engine = create_engine(f"postgresql+psycopg2://postgres:"+PWD_DB+
                       "@database-1-kayak.cp66ow688a77.eu-west-3.rds.amazonaws.com:5432/postgres", 
                       echo=True)

Base = declarative_base()
Base.metadata.create_all(engine)

# Transform
session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
s3 = session.resource("s3")
bucket = s3.Bucket("kayak-booking-datalake-boumrar")
bucket.download_file('35Cities_Weather_Hotels_FINAL.csv', 'data/temp.csv')

dataset = pd.read_csv('data/temp.csv')

# Nettoyage des données
dataset['score'] = dataset['score'].fillna(8.5)

# Nettoyage HTML
for colonne in ['name', 'description']:
    dataset[colonne] = dataset[colonne].str.replace("&#x27;", "'", regex=False)
    dataset[colonne] = dataset[colonne].str.replace("&amp;", "et", regex=False)
    dataset[colonne] = dataset[colonne].str.replace("&quot;", '"', regex=False)
    dataset[colonne] = dataset[colonne].str.replace(r'<[^>]*>', '', regex=True)

# Load
dataset.to_sql(
    "citiesweather",
    engine,
    if_exists="replace"
)

print("ETL terminé!")
