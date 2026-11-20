import pandas as pd
import matplotlib.pyplot as plt

dossier = "C:/Users/ilian zihoune/Desktop/ECOLE_ILIAN_ZIhoune/SAE 15/data/data/"

# Importation des fichiers

support = pd.read_csv(dossier + "sup_support.txt",
                      sep=";", dtype=str, encoding="utf-8")

station = pd.read_csv(dossier + "sup_station.txt",
                      sep=";", dtype=str, encoding="latin-1")

# Fusion des tableaux

fusion = pd.merge(support, station, on="STA_NM_ANFR")

# Suppression des identifiants manquants

fusion = fusion.dropna(subset=["SUP_ID", "ADM_ID"])

# Suppression des associations identiques

fusion = fusion.drop_duplicates(subset=["SUP_ID", "ADM_ID"])

# Nombre d'exploitants par support

exploitants = fusion["SUP_ID"].value_counts()

# Initialisation des compteurs

mutualises = 0
non_mutualises = 0

# Comptage des supports

for nombre in exploitants:

    if nombre >= 2:
        mutualises = mutualises + 1

    else:
        non_mutualises = non_mutualises + 1

# Calcul du pourcentage

total = mutualises + non_mutualises

pourcentage = mutualises / total * 100

# Affichage des resultats

print("Nombre total de supports :", total)
print("Supports mutualises :", mutualises)
print("Supports non mutualises :", non_mutualises)
print("Pourcentage de mutualisation :", pourcentage, "%")

# Graphique

plt.pie([mutualises, non_mutualises],
        labels=["Mutualises", "Non mutualises"],
        autopct="%1.1f%%")

plt.title("Les supports sont-ils mutualises ?")
plt.show()