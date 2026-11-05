# --- 1. Les outils dont on a besoin ---

import json  # pour lire le fichier JSON déjà téléchargé
import os  # pour lire les variables d'environnement (comme le mot de passe)
from datetime import datetime, timezone  # pour convertir le champ "time" en vraie date

import psycopg  # l'outil qui permet à Python de parler à PostgreSQL
from dotenv import load_dotenv  # l'outil qui lit le fichier .env
from psycopg.types.json import Jsonb  # permet d'enregistrer un JSON complet dans une colonne

load_dotenv()  # lit le fichier .env et met son contenu à disposition de Python

# --- 2. Le SQL qui crée la table "brute" ---

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS raw_quakes (
    usgs_id    TEXT PRIMARY KEY,
    event_time TIMESTAMPTZ,
    magnitude  REAL,
    place      TEXT,
    longitude  DOUBLE PRECISION,
    latitude   DOUBLE PRECISION,
    depth_km   DOUBLE PRECISION,
    url        TEXT,
    payload    JSONB
)
"""  # IF NOT EXISTS : ne fait rien si la table existe déjà ; PRIMARY KEY : un identifiant unique par séisme

INSERT = """
INSERT INTO raw_quakes
    (usgs_id, event_time, magnitude, place, longitude, latitude, depth_km, url, payload)
VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (usgs_id) DO NOTHING
"""  # chaque %s sera remplacé par une valeur ; DO NOTHING : si le séisme est déjà là, on ne le recopie pas

# --- 3. Lire le fichier téléchargé ---

with open("data/quakes_2000_2025.json", encoding="utf-8") as fichier:  # ouvre le fichier en lecture
    data = json.load(fichier)  # transforme son contenu en données Python
features = data["features"]  # la liste des séismes

# --- 4. Se connecter à la base et charger les données ---

with psycopg.connect(  # ouvre la connexion ; le "with" valide et ferme tout à la fin
    host="localhost",  # la base tourne sur votre PC (dans Docker)
    port=5432,  # le port qu'on a ouvert dans docker-compose.yml
    dbname="seismic",  # le nom de la base
    user="seismic",  # l'utilisateur
    password=os.environ["POSTGRES_PASSWORD"],  # le mot de passe, lu dans le fichier .env
) as conn:  # "conn" représente la connexion
    with conn.cursor() as cur:  # un "curseur" sert à envoyer des commandes SQL
        cur.execute(CREATE_TABLE)  # crée la table si elle n'existe pas

        nouveaux = 0  # compteur des séismes réellement ajoutés
        for f in features:  # pour chaque séisme de la liste
            props = f["properties"]  # raccourci vers les informations du séisme
            lon, lat, profondeur = f["geometry"]["coordinates"]  # sépare longitude, latitude, profondeur
            date = datetime.fromtimestamp(props["time"] / 1000, timezone.utc)  # millisecondes -> vraie date (UTC)

            cur.execute(INSERT, (  # envoie la commande INSERT avec les 9 valeurs dans l'ordre
                f["id"],  # l'identifiant unique du séisme
                date,  # la date et l'heure
                props["mag"],  # la magnitude
                props["place"],  # le lieu
                lon,  # la longitude
                lat,  # la latitude
                profondeur,  # la profondeur en km
                props["url"],  # l'adresse de la page de l'événement
                Jsonb(f),  # le séisme complet, tel que reçu de l'API (la donnée brute)
            ))
            nouveaux += cur.rowcount  # rowcount vaut 1 si ajouté, 0 si le séisme existait déjà

print("Séismes lus dans le fichier :", len(features))  # combien dans le fichier
print("Séismes ajoutés à la base :", nouveaux)  # combien ont vraiment été ajoutés