# Robotic Fleet Intelligence Platform - Real-Time Air Traffic Monitoring

Robotic Fleet est un projet Data Engineering/ Machine Learning/ Data Analayse de bout en bout, conçu pour explorer toutes les étapes clés d’un workflow complet de gestion et valorisation de données.

L’objectif principal est d’apprendre à concevoir, implémenter et déployer un pipeline de données complet, en partant de la collecte brute jusqu’à la mise à disposition de services intelligents pour les utilisateurs finaux.

Ce projet a été pensé comme un exercice complet et évolutif qui intègre les grandes composantes d'un projet data

C'est à la fois un portfolio technique et un laboratoire d’apprentissage, pensé pour être enrichi continuellement avec :

- des techniques d’optimisation et de scaling en data et en developpement applicatifs.
- des capacités d’analyse prédictive en lien avec les mouvements aériens ou autre (évolutif).
---

## Objectifs du projet (Evolutif)

- Collecter des données aéronautiques en temps réel via une API publique (OpenSky).
- Traiter et transformer les données dans un format exploitable.
- Stocker les données dans une base de données NoSQL (MongoDB).
- Visualiser les données sur une carte interactive et interface client.
- Préparer l'infrastructure pour un déploiement local puis distant.
- Amélioration et test de nouvelles technologies méthodes etc...

---

## Architecture du projet

```bash
├── .gitignore
├── Archive
│   └── test.py
├── Assets
│   ├── description_data.ipynb
│   └── exploratory_analysis.ipynb
├── Backend
│   ├── __pycache__
│   │   └── api_call.cpython-313.pyc
│   ├── api_call.py
│   └── playground-1.mongodb.js
├── Frontend
│   ├── __pycache__
│   │   └── streamlit.cpython-313.pyc
│   └── streamlit_app.py
├── LICENCE.txt
├── README.md
├── Source
│   ├── description_data.csv
│   ├── description_data.xlsx
│   └── openskydata_raw.csv
├── poetry.lock
├── pyproject.toml
└── test.py

```

---

## Sources de données

- **API utilisée** : [OpenSky Network API](https://opensky-network.org/)
- **Données récupérées** : `icao24`, `callsign`, `origin_country`, `latitude`, `longitude`, `altitude`, `velocity`, etc.
- **Zone géographique ciblée** : Munich, Allemagne

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

## Licence

Ce projet est open-source sous licence MIT.