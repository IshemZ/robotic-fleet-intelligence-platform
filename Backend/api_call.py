import requests
import json
import pandas as pd

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("URI_MONGODB")

#OpenSky API base url
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
##data_flights = pd.DataFrame(opensky_data)
#print(data_flights.head())

states = opensky_data.get("states", [])

# Liste des colonnes selon la doc OpenSky
columns = [
    "icao24", "callsign", "origin_country", "time_position", "last_contact",
    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
    "true_track", "vertical_rate", "sensors", "geo_altitude",
    "squawk", "spi", "position_source"
    ]

df = pd.DataFrame(states, columns=columns)

print(df.head())

print(type(df))
print(df.keys())


client = MongoClient(URI)

try:
    client.admin.command('ping')
    print("connexion réussié")
except Exception as e:
    print("Connexion échoué :", e)

db = client["opensky_data"]
collection = db["fleet_intelligence"]

df_json = df.to_dict(orient='records')

results = collection.insert_many(df_json)

print(f"{len(results.inserted_ids)} documents insérés dans mongoDB !")




