import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from Backend.api_call import get_flight_data
load_dotenv()
URI = os.getenv("URI_MONGODB")

#Paramétrage
st.set_page_config(
    page_title="Robotic Fleet Platform",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items= 
    {
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

#Connexion MongoDB
#client = MongoClient(URI)
#db = client["opensky_data"]
#collection = db["fleet_intelligence"]
##Récupération Data et converison dataframe
#data = list(collection.find({}))
#df = pd.DataFrame(data)
#df = df.drop(columns=["_id"])
#df['latitude'] = df['latitude'].astype(float)
#df['longitude'] = df['longitude'].astype(float)

df = get_flight_data()

df = df[df['latitude'].notnull() & df['longitude'].notnull()]
map_data = df[['latitude',"longitude"]]
countries = df["origin_country"].dropna().unique()
countries.sort()

#STREAMLIT INTERFACE 

#SideBar GLobal
with st.sidebar:
    title = st.sidebar.title("Filtre des données")
    filtered_df = df[df["origin_country"].isin(countries)]
    filter_country = st.sidebar.selectbox("Pays", filtered_df)
    Projet2 = st.sidebar.button("Map des avions", use_container_width=True)

#Création des Onglets
tab1, tab2 = st.tabs(["Contexte", "Quelques chiffres"])

#Premier Container de tab1
with tab1.container(border=True):
    st.header("Robotic Fleet Intelligence Platform")
    st.write("*créé par Ishem Zerzour*")
    st.write("L’objectif principal est d’apprendre à concevoir, implémenter et déployer un pipeline de données complet, en partant de la collecte brute jusqu’à la mise à disposition pour les utilisateurs finaux. Ce projet a été pensé comme un exercice complet et évolutif qui intègre les grandes composantes d'un projet data")
    
    #Ajout de 3 colonnes pour mettre les liens de redirection
    col1, col2, col3 = st.columns(3, border=True, vertical_alignment='bottom')
    
    col1.link_button(label="Github Project Repository", url="https://github.com/IshemZ/robotic-fleet-intelligence-platform", type="primary", use_container_width=True)
    col2.link_button(label="LinkedIn", url="https://www.linkedin.com/in/ishem-zerzour/", type='primary', use_container_width=True)
    col3.link_button(label="Ajoute un lien", url="https://www.linkedin.com/in/ishem-zerzour/", type='primary', use_container_width=True)

with tab2.container(border=True):
    st.subheader("Etat du traffic aérien mondial (en temps réel)", divider=True)
    
    
    col4, col5 = st.columns([2,2], border=True, vertical_alignment='top')
    
    col4.map(filtered_df, use_container_width=True, color="#ffaa00", latitude=filtered_df["latitude"], longitude=filtered_df["longitude"])
    col4.dataframe(data=filtered_df)
    
    col5.subheader("KPI")
    col5.write(filtered_df)
    
    col5.subheader("Volume de Vols selon le pays d'origine")
    country_callsign_count = filtered_df.groupby('origin_country')['callsign'].count().reset_index()
    col5.line_chart(data=country_callsign_count.set_index('origin_country')['callsign'])