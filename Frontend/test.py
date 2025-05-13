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
map_data = df[['latitude',"longitude"]]


#STREAMLIT INTERFACE 

#SideBar GLobal
with st.sidebar:
    title = st.sidebar.title("Menu")
    Projet1 =st.sidebar.button("Page d'accueil", use_container_width=True, )
    Projet2 = st.sidebar.button("Map des avions", use_container_width=True)

#Onglet
tab1, tab2 = st.tabs(["Onglet 1", "Onglet 2"])

tab2.subheader("Line Chart")
tab2.line_chart(map_data)
tab2.subheader("Table brut")
tab2.write(map_data)


with tab1.container(border=True):
    st.header("Robotic Fleet Intelligence Platform")
    st.write("*créé par Ishem Zerzour*")
    st.write("L’objectif principal est d’apprendre à concevoir, implémenter et déployer un pipeline de données complet, en partant de la collecte brute jusqu’à la mise à disposition pour les utilisateurs finaux. Ce projet a été pensé comme un exercice complet et évolutif qui intègre les grandes composantes d'un projet data")
    
    col1, col2, col3 = st.columns(3, border=True, vertical_alignment='bottom')
    
    col1.link_button(label="Github Project Repository", url="https://github.com/IshemZ/robotic-fleet-intelligence-platform", type="primary")
    col2.link_button(label="LinkedIn", url="https://www.linkedin.com/in/ishem-zerzour/", type='primary')
    col3.link_button(label="Ajoute un lien", url="https://www.linkedin.com/in/ishem-zerzour/", type='primary')
    
tab1.divider()

with tab1.container(border=True):
    st.subheader("Cartographie", divider=True)
    st.map(map_data, use_container_width=True, color="#ffaa00")
    st.write("Données OpenSky", df)
