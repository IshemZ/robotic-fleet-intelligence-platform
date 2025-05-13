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
#@st.cache

data = list(collection.find({}))
df = pd.DataFrame(data)
df = df.drop(columns=["_id"])

""" 
STREAMLIT INTERFACE

Je vais maintenant construire l'interface utilisateur StreamLit pour présenter le données OpenSky    
"""

#SideBar
add_sidebar = st.sidebar.radio('Accueil')
add_sidebar

#Header
"""st.header('st.button')

st.button('hello')

if st.button('Say Hello'): #bouton cliquable
    st.write('why should i say that') #message en dessous lors du clique
else:
    st.write('goodbye')

st.write("Données OpenSky", df)
st.text_input("Hello")"""

