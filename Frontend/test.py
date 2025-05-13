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
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)
df = df[df['latitude'].notnull() & df['longitude'].notnull()]

#STREAMLIT INTERFACE

#Je vais maintenant construire l'interface utilisateur StreamLit pour présenter le #données OpenSky    

#SideBar
st.sidebar.title("Menu")
vue_global = st.sidebar.segmented_control(options=['Décollage','Atterissage'],label="Etat de l'avion", selection_mode='single')

choix = st.sidebar.selectbox("choisi ton destin", ["Option 1","Option 2"])

Projet1 =st.sidebar.button("Projet 1", use_container_width=True, disabled=False, type="secondary")
Projet2 = st.sidebar.button("Projet 2", key=3)

with st.container(border=True, height=60):
    st.write('Inside')
st.write('Outside')



#Map
map_data = df[['latitude',"longitude"]]
st.map(map_data, use_container_width=True, color="#ffaa00")
df
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

#Header

st.header('Mon Header')

st.button('Mon bouton')

st.write('Hello, *World!* :sunglasses:')

st.write(1212)

if st.button('Say Hello'): #bouton cliquable
    st.write('why should i say that') #message en dessous lors du clique
else:
    st.write('goodbye')
st.subheader('Mon tableau brut')

st.write("Données OpenSky", df)
st.text_input("Hello")



dfo = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
    dfo['first column'])

'You selected: ', option

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)