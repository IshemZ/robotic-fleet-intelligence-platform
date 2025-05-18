import streamlit as st
import pandas as pd
import numpy as np
from math import radians, degrees, cos, sin, atan2, sqrt

# from pymongo import MongoClient
from dotenv import load_dotenv
import os
#from Backend.api_call import get_flight_data

load_dotenv()
URI = os.getenv("URI_MONGODB")

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

#df = get_flight_data()
#df = pd.DataFrame(df)
df = pd.read_csv('Source/openskydata_raw.csv', sep=";")
df = df[df["latitude"].notnull() & df["longitude"].notnull()]
df["origin_country"] = df["origin_country"].fillna("Inconnu")
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

# STREAMLIT INTERFACE

# SideBar GLobal
with st.sidebar:
    title = st.sidebar.title("Filtre des données")
    #country_origin = st.sidebar.selectbox(label="Pays d'origine", sorted(df["origin_country"].unique()), reverse=True)
    pays_input = st.sidebar.selectbox("🌍 Pays d'origine", ["Tous"] + sorted(df["origin_country"].unique().tolist()), key=2)
    
    filtered_df = df.copy()
    if pays_input != "Tous":
        filtered_df = filtered_df[filtered_df["origin_country"] == pays_input]
    source = st.sidebar.link_button("OpenSky Network API", url="https://opensky-network.org/", type='primary', use_container_width=True)
    
#filtrage = df[df["origin_country"] == country_origin]

st.header("Real-Time Air Traffic Monitoring", divider="gray")

# Création des Onglets
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Contexte", "Carte intéractive", "Statistiques & tendances", "Recherche de vol", "Simulation / prévisions", "Bilan & Perspectives"], )

# Premier Container de tab1
with tab1.container(border=True):
    st.write("*créé par Ishem Zerzour*")
    st.write("Cette interface est un projet Data Engineering/ Machine Learning/ Data Analyse de bout en bout, conçu pour explorer toutes les étapes clés d’un workflow complet de gestion et valorisation de données.")
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
    col3.link_button(
        label="Ajoute un lien",
        url="https://www.linkedin.com/in/ishem-zerzour/",
        type="primary",
        use_container_width=True,
    )

#st.dataframe(filtrage, use_container_width=True)

with tab2.container(border=False):
    #st.subheader("Etat du traffic aérien mondial (en temps réel)", divider="gray")

    col4, col5 = st.columns([0.7, 0.3], border=True, vertical_alignment="top")
    if not filtered_df.empty:
        col4.map(filtered_df[["latitude", "longitude"]].dropna())
    #col4.map(
    #    filtered_df,
        use_container_width=True,
        color="#ffaa00",
        latitude=filtered_df["latitude"],
        longitude=filtered_df["longitude"],
    
    st.dataframe(data=filtered_df)

    #col5.subheader("KPI")
    #col5.write(filtered_df)
    col5.subheader("Volume de Vols selon le pays d'origine")
    volume_vols = filtered_df.shape[0]
    col5.metric(label="Nombre de vols", value=f"{volume_vols:,}")
    col5.metric(label="Nombre de vols", value=f"{volume_vols:,}")
    col5.metric(label="Nombre de vols", value=f"{volume_vols:,}")
    col5.metric(label="Nombre de vols", value=f"{volume_vols:,}")
    
with tab3.container(border=True):
    st.title('Statistiques et Tendances')
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Vols aujourd’hui", f"{df.shape[0]:,}")
    col2.metric("Pays impliqués", df["origin_country"].nunique())
    col3.metric("Alt. moyenne (m)", f"{df['baro_altitude'].mean():,.0f}")
    
    st.subheader("✈️ Top compagnies par volume de vols")
    top_compagnies = df["callsign"].dropna().str.slice(0, 3).value_counts().head(20)
    st.bar_chart(top_compagnies)
    
    st.subheader("🌍 Répartition des vols par pays")
    top_pays = df["origin_country"].value_counts().head(20)
    st.bar_chart(top_pays)
    
    st.subheader("📏 Distribution des altitudes (vols en cours)")

    st.bar_chart(df["baro_altitude"].dropna())

with tab4.container(border=True):
    st.title("🔍 Recherche de vol")

    st.markdown("Utilise les filtres ci-dessous pour rechercher un vol dans les données actuelles.")

    # Vérification que le DataFrame est non vide
    if df.empty:
        st.warning("Aucune donnée de vol disponible actuellement.")
        

    # Nettoyage et prétraitement
    df["callsign"] = df["callsign"].fillna("").str.strip()
    df["origin_country"] = df["origin_country"].fillna("Inconnu")

    # --- Filtres de recherche ---
    with st.expander("🔧 Filtres de recherche", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            callsign_input = st.text_input("🔠 Callsign (ex: AFR123)").upper()
            pays_input = st.selectbox("🌍 Pays d'origine", ["Tous"] + sorted(df["origin_country"].unique().tolist()))

        with col2:
            only_in_air = st.checkbox("✈️ Vols en cours (non au sol)", value=True)
            altitude_min = st.slider("🛬 Altitude minimale (m)", 0, 13000, 0)

    # --- Application des filtres ---
    filtered_df = df.copy()

    if callsign_input:
        filtered_df = filtered_df[filtered_df["callsign"].str.contains(callsign_input)]

    if pays_input != "Tous":
        filtered_df = filtered_df[filtered_df["origin_country"] == pays_input]

    if only_in_air:
        filtered_df = filtered_df[filtered_df["on_ground"] == False]

    filtered_df = filtered_df[filtered_df["baro_altitude"].fillna(0) >= altitude_min]

    # --- Résultats ---
    st.subheader(f"🔎 Résultats : {len(filtered_df)} vol(s) trouvé(s)")
    st.dataframe(filtered_df[[
        "icao24","callsign", "origin_country", "baro_altitude", "velocity", "longitude", "latitude", "on_ground"
    ]].rename(columns={
        "icao24": "icao",
        "callsign": "Callsign",
        "origin_country": "Pays",
        "baro_altitude": "Altitude (m)",
        "velocity": "Vitesse (m/s)",
        "longitude": "Longitude",
        "latitude": "Latitude",
        "on_ground": "Au sol"
    }))

    # --- Carte si vols trouvés ---
    if not filtered_df.empty:
        st.map(filtered_df[["latitude", "longitude"]].dropna())

with tab5.container(border=True):

    import numpy as np
    import pandas as pd
    from math import radians, degrees
    import streamlit as st

    def simulate_position(lat, lon, velocity, track_deg, minutes):
        R = 6371e3  # Rayon de la Terre en mètres
        distance = velocity * 60 * minutes  # Distance = vitesse x temps

        lat1 = radians(lat)
        lon1 = radians(lon)
        theta = radians(track_deg)

        lat2 = np.arcsin(np.sin(lat1) * np.cos(distance / R) +
                         np.cos(lat1) * np.sin(distance / R) * np.cos(theta))

        lon2 = lon1 + np.arctan2(np.sin(theta) * np.sin(distance / R) * np.cos(lat1),
                                 np.cos(distance / R) - np.sin(lat1) * np.sin(lat2))

        return degrees(lat2), degrees(lon2)

    def show_simulation_prevision(df):
        st.title("🛰️ Simulation & Prévision de Vol")

        st.markdown("Sélectionne un avion pour simuler sa position dans les prochaines minutes.")

        df = df[df["on_ground"] == False].dropna(subset=["callsign", "latitude", "longitude", "velocity", "true_track"])
        vol_options = df["callsign"].unique().tolist()

        if not vol_options:
            st.warning("Aucun vol actif disponible pour la simulation.")
            return

        selected_callsign = st.selectbox("✈️ Sélectionner un vol (callsign)", vol_options)

        selected_row = df[df["callsign"] == selected_callsign].iloc[0]

        st.markdown(f"**Pays :** {selected_row['origin_country']}")
        st.markdown(f"**Altitude :** {int(selected_row['baro_altitude'] or 0)} m")
        st.markdown(f"**Vitesse :** {int(selected_row['velocity'] or 0)} m/s")
        st.markdown(f"**Direction (°) :** {int(selected_row['true_track'] or 0)}")

        minutes = st.slider("⏱️ Temps de projection (minutes)", 1, 30, 10)

        lat_start, lon_start = selected_row["latitude"], selected_row["longitude"]
        velocity = selected_row["velocity"]
        track = selected_row["true_track"]

        lat_end, lon_end = simulate_position(lat_start, lon_start, velocity, track, minutes)

        st.subheader("📍 Position simulée")
        st.markdown(f"Après **{minutes} minutes**, la position estimée serait :")
        st.code(f"Latitude : {lat_end:.4f} | Longitude : {lon_end:.4f}")

        st.map(pd.DataFrame({
            "latitude": [lat_start, lat_end],
            "longitude": [lon_start, lon_end]
        }, index=["Position actuelle", "Position estimée"]))

        with st.expander("🧮 Données brutes utilisées"):
            st.json({
                "icao24": selected_row["icao24"],
                "callsign": selected_row["callsign"],
                "origin_country": selected_row["origin_country"],
                "longitude": lon_start,
                "latitude": lat_start,
                "velocity (m/s)": velocity,
                "true_track (°)": track,
                "altitude (m)": selected_row["baro_altitude"]
            })

    # Appel de la fonction dans le container
    show_simulation_prevision(filtered_df)  # remplace df_flights par ton DataFrame réel

with tab6.container(border=True):
    st.title("📊 Bilan & Perspectives")

    st.subheader("✅ Ce que j'ai appris")
    st.markdown("""
    - Intégration d'une API en temps réel (OpenSky) pour la récupération des vols en cours.
    - Utilisation avancée de **Streamlit** pour créer une interface interactive.
    - Manipulation de données géographiques et affichage sur carte.
    - Optimisation des performances et structuration du code en modules réutilisables.
    - Meilleure gestion de la mise en page pour un rendu de type **portfolio professionnel**.
    """)

    st.subheader("⚠️ Limites actuelles")
    st.markdown("""
    - Les données de l’API OpenSky sont limitées à certaines régions (notamment en dehors de l’Europe).
    - Rafraîchissement des données pas encore automatisé (statique à l’ouverture).
    - Pas encore d'analyse approfondie des retards ou des itinéraires.
    - Pas de persistance des données (pas de base de données locale ou cloud).
    """)

    st.subheader("🚀 Améliorations futures")
    st.markdown("""
    - Ajouter un système de **cache ou base de données** pour stocker l'historique des vols.
    - Intégrer d'autres APIs (météo, aéroports, compagnies) pour enrichir l’analyse.
    - Proposer des **prédictions de retard** avec un modèle de machine learning.
    - Ajouter des filtres par pays, compagnie ou altitude.
    - Export des données personnalisées (CSV/Excel).
    - Déploiement de l'app via **Streamlit Cloud** ou autre plateforme avec monitoring.
    """)

    st.success("Tu veux en savoir plus ? Consulte le code source sur [GitHub](https://github.com/ton-repo) ou contacte-moi pour discuter !")