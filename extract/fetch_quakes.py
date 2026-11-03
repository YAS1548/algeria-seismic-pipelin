# --- 1. Les outils dont on a besoin ---

import json  # outil pour lire et écrire des fichiers au format JSON
from datetime import datetime, timezone  # outils pour manipuler des dates et des fuseaux horaires
from pathlib import Path  # outil pour gérer des dossiers et des chemins de fichiers

import requests  # outil (installé avec pip) pour appeler une adresse web

# --- 2. Les réglages de la requête ---

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"  # adresse de l'API de l'USGS

params = {  # un "dictionnaire" : une liste de réglages sous la forme nom: valeur
    "format": "geojson",  # on demande la réponse au format GeoJSON (un JSON géographique)
    "starttime": "2025-01-01",  # date de début : on garde les séismes à partir d'ici
    "endtime": "2025-12-31",  # date de fin : on garde les séismes jusqu'ici
    "minlatitude": 18,  # côté sud du rectangle de recherche
    "maxlatitude": 38,  # côté nord du rectangle
    "minlongitude": -9,  # côté ouest du rectangle
    "maxlongitude": 12.5,  # côté est du rectangle
    "minmagnitude": 3,  # on ignore les séismes de magnitude inférieure à 3
}

# --- 3. L'appel à l'API ---

response = requests.get(URL, params=params, timeout=30)  # envoie la demande ; abandonne après 30 secondes
response.raise_for_status()  # si l'API répond par une erreur, le script s'arrête avec un message clair
data = response.json()  # transforme la réponse en données Python (dictionnaires et listes)

# --- 4. Lire les données ---

features = data["features"]  # la liste des séismes (un élément = un séisme)
print("Nombre de séismes :", len(features))  # len() compte les éléments de la liste, print() affiche

for f in features[:5]:  # boucle sur les 5 premiers séismes ; "f" est le séisme en cours
    props = f["properties"]  # raccourci vers les informations du séisme (magnitude, lieu, date...)
    lon, lat, profondeur = f["geometry"]["coordinates"]  # sépare les 3 valeurs, dans cet ordre
    date = datetime.fromtimestamp(props["time"] / 1000, timezone.utc)  # convertit les millisecondes en vraie date (UTC)
    print(  # affiche une ligne avec les informations principales, séparées par " | "
        date.strftime("%Y-%m-%d %H:%M"),  # la date écrite comme 2025-03-14 08:25
        "| M", props["mag"],  # la magnitude
        "|", props["place"],  # le lieu
        "|", lat, lon,  # la latitude puis la longitude
    )

# --- 5. Sauvegarder dans un fichier ---

Path("data").mkdir(exist_ok=True)  # crée le dossier "data" s'il n'existe pas déjà (sans erreur sinon)
with open("data/quakes_2025.json", "w", encoding="utf-8") as fichier:  # ouvre le fichier en écriture ("w") ; "with" le referme tout seul
    json.dump(data, fichier, ensure_ascii=False, indent=2)  # écrit les données ; garde les accents ; indente pour que ce soit lisible
print("Fichier enregistré : data/quakes_2025.json")  # message de confirmation