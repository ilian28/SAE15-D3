# SAE-15--Traiter-des-donn-es
Analyse des installations radioélectriques en France

HOW TO USE

- GENERETATE_MAP.IPYNB (SAE15) -
Ce module permet de charger les données de supports d'antennes (`sup_support.txt`), de convertir les coordonnées DMS en degrés décimaux, de classer les antennes par opérateur (`TPO_ID`) et de générer une carte interactive exploitable dans **Jupyter Notebook** et dans un **navigateur web**, accompagnée d'une archive `.zip` compressée.
Pensez à indiquer le bon chemin, où se trouve votre carte html, ainsi que le chemin de votre fichier source.

Installation :
pandas
folium

- CARTE_ANTENNES_FRANCE.ZIP -
une carte au format html compressée pour faciliter la réception des données, fonctionne avec le fichier 'generate_map.ipynb'
