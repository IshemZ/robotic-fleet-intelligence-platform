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

#SideBar
with st.sidebar:
    title = st.sidebar.title("Menu")
    Projet1 =st.sidebar.button("Page d'accueil", use_container_width=True, )
    Projet2 = st.sidebar.button("Map des avions", use_container_width=True)
    

#Onglet
tab1, tab2 = st.tabs(["Onglet 1", "Onglet 2"])
data = np.random.randn(10, 1)

tab2.subheader("A tab with a chart")
tab2.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)


with tab1.container(border=True):
    tab1.header("Robotic Fleet Intelligence Platform")
    tab1.write("*créé par Ishem Zerzour*")
    tab1.write("L’objectif principal est d’apprendre à concevoir, implémenter et déployer un pipeline de données complet, en partant de la collecte brute jusqu’à la mise à disposition pour les utilisateurs finaux. Ce projet a été pensé comme un exercice complet et évolutif qui intègre les grandes composantes d'un projet data")
    
    #tab1.divider()
    
    col1, col2, col3 = tab1.columns(3, border=True, vertical_alignment='bottom')
    #with col1:
    col1.link_button(label="Github Project Repository", url="https://github.com/IshemZ/robotic-fleet-intelligence-platform", type="primary")
    #with col2:
    col2.link_button(label="LinkedIn", url="https://www.linkedin.com/in/ishem-zerzour/", type='primary')
    #with col3:
    col3.link_button(label="Ajoute un lien", url="https://www.linkedin.com/in/ishem-zerzour/", type='primary')

with tab1.container(border=True):
    st.subheader("Cartographie", divider=True)
    st.map(map_data, use_container_width=True, color="#ffaa00")
    st.write("Données OpenSky", df)
