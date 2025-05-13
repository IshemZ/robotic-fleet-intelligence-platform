import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

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
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)
df = df[df['latitude'].notnull() & df['longitude'].notnull()]


#SideBar
st.sidebar.title("Menu")
vue_global = st.sidebar.segmented_control(options=['Décollage','Atterissage'],label="Etat de l'avion", selection_mode='single')

choix = st.sidebar.selectbox("choisi un pays", ["France","Allemagne"])

Projet1 =st.sidebar.button("Vue 1", use_container_width=True, disabled=False, type="secondary")
Projet2 = st.sidebar.button("Vue 2", use_container_width=True)

#Map
map_data = df[['latitude',"longitude"]]
st.map(map_data, use_container_width=True, color="#ffaa00")
df