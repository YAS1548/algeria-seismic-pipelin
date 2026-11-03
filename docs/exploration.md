# Exploration de l'API USGS

## Où se trouvent les informations
- Magnitude : dans features → properties → mag
- Lieu : dans features -> properties -> place
- Date : dans features -> properties -> time
- Coordonnées : dans features -> geometry -> coordinates
- URL : dans features -> properties -> url

## Ce que j'ai remarqué
- Le champ "time" est un grand nombre : des millisecondes écoulées depuis le 1er janvier 1970.
- L'ordre des coordonnées est : [longitude, latitude, profondeur en km]

## Nombre de séismes (requêtes testées)
- 2025, magnitude 3 minimum :16 séismes
- 2024, magnitude 3 minimum : 13 séismes

## Problèmes de qualité des données
- Dans "place", certains séismes sont au Maroc, en Tunisie, en mer : que deux qui mentionne lalgerie donc pas assez dinformation la concernat

## Ce que ça implique pour le projet
- Environ 15 séismes par an : trop peu pour un seul an
- Sur 2000-2025 : 2657 séismes
- Seulement 2 sur 16 mentionnent l'Algérie : il faudra filtrer
- beaucoup plus d’événements avant : à comprendre (séisme majeur et répliques ? zone trop large ?)
