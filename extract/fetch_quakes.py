# Les outils ont on a besoin 

import json
from collections import  Counter  #outil pour compter combien de fois chaque valeur apparaît
from datetime import datetime, timezone
from pathlib import Path # outil pour gérer des dossiers et des chemins



with open("data/quakes_2000_2025.json", encoding="utf-8") as fichier:
    data = json.load(fichier)


features = data["features"]



for annee in [2003, 2004, 2009]:  # on répète ce qui suit pour chacune de ces années
    pays = Counter()  # un compteur vide pour compter les séismes par pays
    plus_fort = None  # on garde ici le séisme le plus fort (vide au début)

    for f in features:  # on parcourt tous les séismes
        props = f["properties"]  # raccourci vers les informations du séisme
        date = datetime.fromtimestamp(props["time"] / 1000, timezone.utc)  # convertit "time" en vraie date
        if date.year != annee:  # si le séisme n'est pas de l'année étudiée
            continue  # on passe directement au séisme suivant

        lieu = props["place"] or ""  # le lieu ; texte vide s'il est absent
        nom_pays = lieu.split(",")[-1].strip()  # garde ce qui suit la dernière virgule (le pays) et enlève les espaces
        pays[nom_pays] += 1  # ajoute 1 au compteur de ce pays

        mag = props["mag"]  # la magnitude de ce séisme
        if mag is not None and (plus_fort is None or mag > plus_fort[0]):  # si c'est le plus fort vu jusqu'ici
            plus_fort = (mag, lieu)  # on retient sa magnitude et son lieu

    print(annee, "| par pays :", dict(pays))  # affiche le nombre de séismes par pays
    print(annee, "| plus fort :", plus_fort)  # affiche le séisme le plus fort de l'année