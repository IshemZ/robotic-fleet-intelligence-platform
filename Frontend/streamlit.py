import streamlit as st
import pandas as pd

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("URI_MONGODB")

#Connexion MongoDB
client = MongoClient(URI)
db = client["opensky_data"]
collection = db["fleet_intelligence"]

#Récupération Data et converison dataframe
data = list(collection.find({}))
df = pd.DataFrame(data)
df = df.drop(columns=["_id"])
st.write("Données OpenSky", df)

