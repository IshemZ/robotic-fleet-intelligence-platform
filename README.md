# Robotic Fleet - Real-Time Air Traffic Monitoring

**Robotic Fleet** est un projet Data Engineering de bout en bout qui utilise l’API OpenSky Network pour collecter des données de trafic aérien en temps réel, les stocke dans une base MongoDB, et les rend disponibles pour visualisation via une interface utilisateur.

---

## Objectifs du projet

- Collecter des données aéronautiques en temps réel via une API publique (OpenSky).
- Traiter et transformer les données dans un format exploitable.
- Stocker les données dans une base de données NoSQL (MongoDB).
- Visualiser les données sur une carte interactive.
- Préparer l'infrastructure pour un déploiement local puis distant.

---

## Architecture du projet

---

## Sources de données

- **API utilisée** : [OpenSky Network API](https://opensky-network.org/)
- **Données récupérées** : `icao24`, `callsign`, `origin_country`, `latitude`, `longitude`, `altitude`, `velocity`, etc.
- **Zone géographique ciblée** : Munich, Allemagne (modifiable)

---

## Fonctionnalités

- Récupération des données en temps réel via un appel API
- Transformation en `pandas.DataFrame`
- Export CSV pour suivi local
- Insertion des données dans MongoDB
- Visualisation cartographique interactive (en cours)
- Déploiement distant (prévu)

---

## Installation

1. Clone ce repo :

```bash
git clone https://github.com/IshemZ/robotic-fleet-intelligence-platform
cd robotic-fleet-intelligence-platform
```

2. Crée un environnement virtuel (Poetry) et installe les dépendances :

```bash
pip install poetry
poetry install
poetry shell
```

## Utilisation

Lancer la collecte de données :

```bash
cd backend
python fetch_opensky_data.py
```

## Visualisation à venir

L’interface de visualisation sera développée avec :
• Streamlit ou Plotly Dash
• Intégration d’une carte interactive (ex. folium, deck.gl)
• Dashboard en temps réel avec mise à jour automatique.

## Roadmap
• Appel API OpenSky
• Transformation des données
• Insertion MongoDB
• Visualisation sur carte interactive
• Déploiement sur serveur distant
• Interface utilisateur finale

## Cas d’usage envisagés
• Suivi de flotte pour entreprises aéro
• Analyse de comportements de vol
• Visualisation de trafic aérien en temps réel
• Intégration avec systèmes IoT/robotique (plus tard)

## Licence

Ce projet est open-source sous licence MIT.