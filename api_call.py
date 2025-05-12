import requests
import json
import pandas as pd

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





'''
# Vérifie que la requête s'est bien passée (code 200)
if response.status_code == 200:
    data = response.json()
    print("Voici les 3 premiers posts :")
    for post in data[:3]: #affichage uniquement 3 premiers
        print(f"ID: {post['id']} - Titre: {post['title']}")
else:
    print("Erreur lors de l'appel API :", response.status_code)

'''



