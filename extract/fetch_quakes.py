# Les outils ont on a besoin 

import json
from collections import  Counter  #outil pour compter combien de fois chaque valeur apparaît
from datetime import datetime, timezone
from pathlib import Path # outil pour gérer des dossiers et des chemins

import requests #outils pour appler une adresse web 

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"  # adresse de l'API de l'USGS

# utiliser une fonction pour reutiliser lee code

def fetch_quakes(starttime, endtime):
    params = {
      "format": "geojson",
      "starttime": starttime,
      "endtime": endtime,
      "minlatitude": 18,
      "maxlatitude": 38,
      "minlongitude": -9,
      "maxlongitude": 12.5,
      "minmagnitude": 3,

     }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()    
    return response.json()

#---------
data = fetch_quakes("2000-01-01", "2025-12-31")
features = data["features"]
print("Nombre de séisme:", len(features))


par_annee = Counter()
for f in features:
    date = datetime.fromtimestamp(f["properties"]["time"]/ 1000, timezone.utc) # convertit "time" en vraie date
    par_annee[date.year] += 1 # ajoute 1 au compteur de l'année de ce séisme

for annee in sorted(par_annee): #parcours les annee dans lordre croissannt
    print(annee, ":", par_annee[annee], "séisme")    


#-----Compter ceux qui mentionnent lalgerie
nb_algerie = 0
for f in features:
    lieu = f["properties"]["place"] or ""
    if "Algeria" in lieu:
        nb_algerie += 1
print("Dont mentionnent l'Algérie :", nb_algerie)

#-----sauvegarde dans un fichier

Path("data").mkdir(exist_ok=True) # crée le dossier "data" s'il n'existe pas
with open ("data/quakes_2000_2025.json", "w", encoding="utf-8") as fichier:
    json.dump(data, fichier, ensure_ascii=False, indent=2)

print("Fichier enregistré : data/quakes_2000_2025.json")