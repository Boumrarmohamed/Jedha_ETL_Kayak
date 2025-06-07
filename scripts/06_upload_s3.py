import boto3
import os
from dotenv import load_dotenv
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Créer la session AWS
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Créer le client S3
s3 = session.resource('s3')

# Configuration pour la région Europe (Paris)
CreateBucketConfiguration = {
    'LocationConstraint': 'eu-west-3',
}

# Récupérer le bucket existant
bucket = s3.Bucket("kayak-booking-datalake-boumrar")

# Upload du fichier CSV
bucket.upload_file('./data/35Cities_Weather_Hotels_FINAL.csv', '35Cities_Weather_Hotels_FINAL.csv')

print("Upload terminé!")
