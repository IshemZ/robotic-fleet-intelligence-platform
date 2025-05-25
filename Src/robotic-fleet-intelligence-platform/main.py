import streamlit as st
import pandas as pd
import numpy as np
from math import radians, degrees
import pandas as pd
import requests
from datetime import datetime
import json
from PIL import Image
# from Backend.api_call import get_flight_data
# from pymongo import MongoClient
# from dotenv import load_dotenv
import os

# load_dotenv()
# URI = os.getenv("URI_MONGODB")

# Paramétrage
st.set_page_config(
    page_title="Robotic Fleet Platform",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)
# import pandas as pd
# import requests
# from dotenv import load_dotenv
# from datetime import datetime
# from pymongo import MongoClient
# import json
# import os
# import streamlit as st
# load_dotenv()

# URI = os.getenv("URI_MONGODB")

# OpenSky API base url
url = "https://opensky-network.org/api/states/all"

@st.cache_data(ttl=3600)
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

if opensky_data is not None:
    states = opensky_data.get("states", [])
else:
    states = []

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
df.head()

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


# Connexion MongoDB
# client = MongoClient(URI)
# db = client["opensky_data"]
# collection = db["fleet_intelligence"]

# Récupération Data et converison dataframe
# data = list(collection.find({}))
# df = pd.DataFrame(data)
# df = df.drop(columns=["_id"])
# df['latitude'] = df['latitude'].astype(float)
# df['longitude'] = df['longitude'].astype(float)

df = get_flight_data()
df = pd.DataFrame(df)
# df = pd.read_csv("Source/openskydata_raw.csv", sep=";")
df = df[df["latitude"].notnull() & df["longitude"].notnull()]
df["origin_country"] = df["origin_country"].fillna("Inconnu")
df["latitude"] = df["latitude"].astype(float) 
df["longitude"] = df["longitude"].astype(float)

# STREAMLIT INTERFACE

with st.sidebar:
    st.title("Filtre des données")

    pays_input = st.selectbox(
        "Pays d'origine",
        ["Tous"] + sorted(df["origin_country"].unique().tolist()),
        key="pays_input",
    )
    altitude_min = st.slider("Altitude minimale (m)", 0, int(df["baro_altitude"].max()), 0)
    vitesse_min = st.slider("Vitesse minimale (km/h)", 0, 1000, 0)

    filtered_df = df.copy()
    if pays_input != "Tous":
        filtered_df = filtered_df[filtered_df["origin_country"] == pays_input]
    filtered_df = filtered_df[
        (filtered_df["baro_altitude"] >= altitude_min) &
        (filtered_df["velocity"] >= vitesse_min)
    ]

    st.divider()
    st.markdown("**Données provenant de :**")
    st.link_button(
        "OpenSky Network API",
        url="https://opensky-network.org/",
        type="primary",
        use_container_width=True, 
    )

    st.markdown("---")
    st.markdown(" **Contact développeur :** [ishem.zerzour@gmail.com](mailto:ishem.zerzour@gmail.com)")

# filtrage = df[df["origin_country"] == country_origin]

st.header("Real-Time Air Traffic Monitoring", divider="gray")

# Création des Onglets
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Contexte",
        "Carte intéractive",
        "Statistiques & tendances",
        "Recherche de vol",
        "Simulation / prévisions",
        "Bilan & Perspectives",
    ],
)

# Premier Container de tab1
with tab1.container(border=True):
    st.write("*créé par Ishem Zerzour*")
    st.write(
        "Cette interface est un projet Data Engineering/"
        "Machine Learning/ Data Analyse de bout en bout, "
        "conçu pour explorer toutes les étapes clés d’un workflow "
        "complet de gestion et valorisation de données."
    )
    st.write(
        "L’objectif principal est d’apprendre à concevoir, "
        "implémenter et déployer un pipeline de données complet "
        "en partant de la collecte brute jusqu’à la mise à disposition "
        "pour les utilisateurs finaux. Ce projet a été pensé "
        "comme un exercice complet et évolutif "
        "qui intègre les grandes composantes d'un projet data"
    )

    # Ajout de 3 colonnes pour mettre les liens de redirection
    col1, col2, col3 = st.columns(3, border=False, vertical_alignment="center")

    col1.link_button(
        label="Github Project Repository",
        url="https://github.com/IshemZ/robotic-fleet-intelligence-platform",
        type="primary",
        use_container_width=True,
    )
    col2.link_button(
        label="LinkedIn",
        url="https://www.linkedin.com/in/ishem-zerzour/",
        type="primary",
        use_container_width=True,
    )
    # col3.link_button(
    #    label="Envoyer un message",
    #    url="mailto:zerzourishem@gmail.com",
    #    type="primary",
    #    use_container_width=True,
    # )
    col3.markdown("""
    <a href="mailto:zerzourishem@gmail.com?subject=Demande%20de%20contact&body=Bonjour Ishem,%20je%20souhaite%20échanger%20avec%20vous."
    style="
        display: inline-block;
        width: 100%;
        text-align: center;
        padding: 8px 80px;
        font-size: 16px;
        color: white;
        background-color: #284EA0;
        text-decoration: none;
        border-radius: 8px;
    ">
        Me contacter par mail
    </a>
""", unsafe_allow_html=True,)


    tab1.markdown("### ")
    from PIL import Image
    image = Image.open("photo.jpg")
    tab1.image(
        image,
        caption="Vue aérienne",
    
    )


    tab1.markdown("---")


    tab1.markdown(
    "<p style='text-align: center; font-size: 14px; color: grey;'>© 2025 - Projet développé par Ishem Zerzour.</p>",
    unsafe_allow_html=True
    )

    tab1.info("Dernière mise à jour : Mai 2025 - Version 1.0.0")


    if tab1.button("Laisser un feedback "):
        tab1.toast("Merci pour votre retour (fonctionnalitée à venir)")

with tab2.container(border=False):
    # st.subheader("Etat du traffic aérien mondial (en temps réel)", divider="gray")

    col4, col5 = st.columns([0.7, 0.3], border=True, vertical_alignment="top")
    if not filtered_df.empty:
        col4.map(filtered_df[["latitude", "longitude"]].dropna(), )
        # col4.map(
        #    filtered_df,
        use_container_width = (True,)
        color = ("#E69B06",)
        latitude = (filtered_df["latitude"],)
        longitude = (filtered_df["longitude"],)

    st.dataframe(data=filtered_df)

    col5.subheader("KPI")
    volume_vols = filtered_df.shape[0]
    nb_pays = filtered_df["origin_country"].nunique()
    altitude_moy = filtered_df["baro_altitude"].mean()
    vitesse_moy = filtered_df["velocity"].mean()
    nb_au_sol = filtered_df["on_ground"].sum()
    nb_en_air = volume_vols - nb_au_sol

    # col5.metric(label="Nombre de vols total", value=f"{volume_vols:,}")
    col5.metric(label="Vols en l’air", value=f"{nb_en_air:,}")
    col5.metric(label="Vols au sol", value=f"{nb_au_sol:,}")
    col5.metric(label="Pays représentés", value=f"{nb_pays:,}")
    col5.metric(label="Altitude moyenne (m)", value=f"{altitude_moy:,.0f} m")
    col5.metric(label="Vitesse moyenne (m/s)", value=f"{vitesse_moy:,.0f} m/s")

with tab3.container(border=False):
    st.title("Statistiques et Tendances")

    col1, col2, col3 = st.columns(3)
    col1.metric("Vols aujourd’hui", f"{df.shape[0]:,}")
    col2.metric("Pays impliqués", df["origin_country"].nunique())
    col3.metric("Alt. moyenne (m)", f"{df['baro_altitude'].mean():,.0f}")

    st.subheader("Top compagnies par volume de vols")
    top_compagnies = df["callsign"].dropna().str.slice(0, 3).value_counts().head(20)
    st.bar_chart(top_compagnies)

    st.subheader("Répartition des vols par pays")
    top_pays = df["origin_country"].value_counts().head(20)
    st.bar_chart(top_pays)

    st.subheader("Distribution des altitudes (vols en cours)")

    st.bar_chart(df["baro_altitude"].dropna())

with tab4.container(border=False):
    st.title("Recherche de vol")

    st.markdown(
        "Utilise les filtres ci-dessous pour rechercher un vol dans les données actuelles."
    )

    # Vérification que le DataFrame est non vide
    if df.empty: 
        st.warning("Aucune donnée de vol disponible actuellement.")

    # Nettoyage et prétraitement
    df["callsign"] = df["callsign"].fillna("").str.strip()
    df["origin_country"] = df["origin_country"].fillna("Inconnu")

    # --- Filtres de recherche ---
    with st.expander("Filtres de recherche", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            callsign_input = st.text_input("Callsign (ex: AFR123)").upper()
            pays_input = st.selectbox(
                "Pays d'origine",
                ["Tous"] + sorted(df["origin_country"].unique().tolist()),
            )

        with col2:
            only_in_air = st.checkbox("Vols en cours (non au sol)", value=True)
            altitude_min = st.slider("Altitude minimale (m)", 0, 13000, 0)

    # --- Application des filtres ---
    filtered_df = df.copy()

    if callsign_input:
        filtered_df = filtered_df[filtered_df["callsign"].str.contains(callsign_input)]

    if pays_input != "Tous":
        filtered_df = filtered_df[filtered_df["origin_country"] == pays_input]

    if only_in_air is False:
        filtered_df = filtered_df[filtered_df["on_ground"]]

    filtered_df = filtered_df[filtered_df["baro_altitude"].fillna(0) >= altitude_min]

    # --- Résultats ---
    st.subheader(f" Résultats : {len(filtered_df)} vol(s) trouvé(s)")
    st.dataframe(
        filtered_df[
            [
                "icao24",
                "callsign",
                "origin_country",
                "baro_altitude",
                "velocity",
                "longitude",
                "latitude",
                "on_ground",
            ]
        ].rename(
            columns={
                "icao24": "icao",
                "callsign": "Callsign",
                "origin_country": "Pays",
                "baro_altitude": "Altitude (m)",
                "velocity": "Vitesse (m/s)",
                "longitude": "Longitude",
                "latitude": "Latitude",
                "on_ground": "Au sol",
            }
        )
    )

    # --- Carte si vols trouvés ---
    if not filtered_df.empty:
        st.map(filtered_df[["latitude", "longitude"]].dropna())

with tab5.container(border=False):

    def simulate_position(lat, lon, velocity, track_deg, minutes):
        R = 6371e3  # Rayon de la Terre en mètres
        distance = velocity * 60 * minutes  # Distance = vitesse x temps

        lat1 = radians(lat)
        lon1 = radians(lon)
        theta = radians(track_deg)

        lat2 = np.arcsin(
            np.sin(lat1) * np.cos(distance / R)
            + np.cos(lat1) * np.sin(distance / R) * np.cos(theta)
        )

        lon2 = lon1 + np.arctan2(
            np.sin(theta) * np.sin(distance / R) * np.cos(lat1),
            np.cos(distance / R) - np.sin(lat1) * np.sin(lat2),
        )

        return degrees(lat2), degrees(lon2)
    
    st.title("Simulation & Prévision de Vol")

    st.markdown(
            "Sélectionnez un avion pour simuler sa position dans les prochaines minutes.")
    st.markdown(
            "Cette simulation est basée sur la vitesse et la direction actuelles du vol.")
    st.markdown(
            "Note : Les données de l'API OpenSky sont mises à jour toutes les 10 secondes, "
            "donc la simulation peut ne pas être précise à long terme."
        )
    col8, col9 = st.columns(2, border=True)
    
    def show_simulation_prevision(df):

        df = df[df["on_ground"] == False].dropna(
            subset=["callsign", "latitude", "longitude", "velocity", "true_track"]
        )
        vol_options = df["callsign"].unique().tolist()

        if not vol_options:
            st.warning("Aucun vol actif disponible pour la simulation.")
            return

        selected_callsign = col8.selectbox(
            "Sélectionner un vol (callsign)", vol_options
        )

        selected_row = df[df["callsign"] == selected_callsign].iloc[0]

        col9.markdown(f"**Pays :** {selected_row['origin_country']}")
        col9.markdown(f"**Altitude :** {int(selected_row['baro_altitude'] or 0)} m")
        col9.markdown(f"**Vitesse :** {int(selected_row['velocity'] or 0)} m/s")
        col9.markdown(f"**Direction (°) :** {int(selected_row['true_track'] or 0)}")

        minutes = col8.slider("Temps de projection (minutes)", 1, 30, 10)

        lat_start, lon_start = selected_row["latitude"], selected_row["longitude"]
        velocity = selected_row["velocity"]
        track = selected_row["true_track"]

        lat_end, lon_end = simulate_position(
            lat_start, lon_start, velocity, track, minutes
        )

        st.subheader("Position simulée")
        st.markdown(f"Après **{minutes} minutes**, la position estimée serait :")
        st.code(f"Latitude : {lat_end:.4f} | Longitude : {lon_end:.4f}")

        st.map(
            pd.DataFrame(
                {"latitude": [lat_start, lat_end], "longitude": [lon_start, lon_end]},
                index=["Position actuelle", "Position estimée"],
            )
        )

        with st.expander("Données brutes utilisées"):
            st.json(
                {
                    "icao24": selected_row["icao24"],
                    "callsign": selected_row["callsign"],
                    "origin_country": selected_row["origin_country"],
                    "longitude": lon_start,
                    "latitude": lat_start,
                    "velocity (m/s)": velocity,
                    "true_track (°)": track,
                    "altitude (m)": selected_row["baro_altitude"],
                }
            )  

    # Appel de la fonction dans le container
    show_simulation_prevision(filtered_df)  # remplace df_flights par ton DataFrame réel

with tab6.container(border=True):
    st.title("Bilan & Perspectives")

    st.subheader("Ce que j'ai appris")
    st.markdown(
        """
    - Intégration d'une API en temps réel (OpenSky) pour la récupération des vols en cours.
    - Utilisation avancée de **Streamlit** pour créer une interface interactive.
    - Manipulation de données géographiques et affichage sur carte.
    - Optimisation des performances et structuration du code en modules réutilisables.
    - Meilleure gestion de la mise en page pour un rendu de type **portfolio professionnel**.
    """
    )

    st.subheader("Limites actuelles")
    st.markdown(
        """
    - Les données de l’API OpenSky sont limitées à certaines régions (notamment en dehors de l’Europe).
    - Rafraîchissement des données pas encore automatisé (statique à l’ouverture).
    - Pas encore d'analyse approfondie des retards ou des itinéraires.
    - Pas de persistance des données (pas de base de données locale ou cloud).
    """
    )

    st.subheader("Améliorations futures")
    st.markdown(
        """
    - Ajout d'un système de **cache ou base de données** pour stocker l'historique des vols.
    - Intégrer d'autres APIs (météo, aéroports, compagnies) pour enrichir l’analyse.
    - Proposer des **prédictions de retard** avec un modèle de machine learning.
    - Ajouter des filtres par pays, compagnie ou altitude.
    - Export des données personnalisées (CSV/Excel).
    - Déploiement de l'app via **Streamlit Cloud** ou autre plateforme avec monitoring.
    """
    )

    st.success(
        "Merci d'avoir pris le temps de me lire !"
    )
