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

##  Remarque :pics en 2003-2005, chute en 2009 : à expliquer...
2003 | par pays : {'Algeria': 255, 'Spain': 29, 'Morocco': 13, 'Tunisia': 3, 'northern Algeria': 5, 'western Mediterranean Sea': 1, 'Portugal': 1}
2003 | plus fort : (6.8, '25 km WNW of Dellys, Algeria')
2004 | par pays : {'Spain': 16, 'Morocco': 879, 'Algeria': 53, 'Strait of Gibraltar': 16, 'Tunisia': 1, 'Portugal': 11}
2004 | plus fort : (6.4, '11 km SSW of Tirhanimîne, Morocco')
2009 | par pays : {'Algeria': 6, 'Morocco': 2, 'Portugal': 2}
2009 | plus fort : (4.9, '48 km ENE of Aïn Sefra, Algeria')
