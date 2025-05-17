import requests

# import json
import pandas as pd

# from datetime import datetime
# from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("URI_MONGODB")

# OpenSky API base url
url = "https://opensky-network.org/api/states/all"


def fetchFlightData():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occured: {e}")
        return None


opensky_data = fetchFlightData()

states = opensky_data.get("states", [])

# Liste des colonnes selon la doc OpenSky
columns = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]

df = pd.DataFrame(states, columns=columns)

column_dtypes = {
    "icao24": str,  # identifiant avion (base36)
    "callsign": str,  # appel radio (souvent string, parfois null)
    "origin_country": str,  # pays d'origine (string)
    "time_position": int,  # timestamp (en float ou int UNIX)
    "last_contact": int,  # timestamp (UNIX)
    "longitude": float,  # coordonnées GPS
    "latitude": float,
    "baro_altitude": float,  # altitude barométrique (peut être None)
    "on_ground": bool,  # booléen (True/False)
    "velocity": float,  # vitesse (m/s)
    "true_track": float,  # direction réelle (angle degrés)
    "vertical_rate": float,  # taux de montée/descente (m/s)
    "sensors": str,  # liste de capteurs (peut être None ou [])
    "geo_altitude": float,  # altitude géométrique (m)
    "squawk": str,  # code transpondeur (souvent 4 chiffres, parfois None)
    "spi": bool,  # position spéciale (bool)
    "position_source": int,  # source de position (0, 1, 2 selon spec OpenSky)
}

df["last_contact"] = df["last_contact"].astype(float)
df["time_position"] = df["time_position"].astype(float)
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)
df["baro_altitude"] = df["baro_altitude"].astype(float)
df["velocity"] = df["velocity"].astype(float)
df["true_track"] = df["true_track"].astype(float)
df["vertical_rate"] = df["vertical_rate"].astype(float)
df["geo_altitude"] = df["geo_altitude"].astype(float)
df["position_source"] = df["position_source"].astype(int)
df["on_ground"] = df["on_ground"].astype(bool)
df["spi"] = df["spi"].astype(bool)
df["last_contact"] = pd.to_datetime(df["last_contact"], unit="s", errors="coerce")
df["time_position"] = pd.to_datetime(df["time_position"], unit="s", errors="coerce")
df

# Extract CSV pour échantillons
df_csv = df.copy()
df_csv.to_csv(
    "../robotic-fleet-intelligence-platform/Source/openskydata_raw.csv",
    sep=";",
    index=False,
)


# encapsuler le df dans une fonction pour l'appeler dans un autre script
def get_flight_data():
    flight_data = df
    return flight_data


"""client = MongoClient(URI)
db = client["opensky_data"]
collection = db["fleet_intelligence"]

try:
    client.admin.command('ping')
    print("connexion réussié")
except Exception as e:
    print("Connexion échoué :", e)

#supprimer les élements précédents existants sur la bdd mongoDB
collection.delete_many({})

#Dataframe to Json -> envoi à la base de données MongoDB
df_json = df.to_dict(orient='records')

results = collection.insert_many(df_json)

print(f"{len(results.inserted_ids)} documents insérés dans mongoDB !")"""
