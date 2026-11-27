
import pandas as pd
import matplotlib.pyplot as plt

# Chemins vers les dossiers de donnees
dossier = r"C:\Users\ordi2405609\Desktop\BUT-1\SAE15\data\data"
dossier_ref = r"C:\Users\ordi2405609\Desktop\BUT-1\SAE15\ref\ref"

# Recuperer les fichiers des supports et de leurs proprietaires
support = pd.read_csv(
    dossier + r"\sup_support.txt",
    sep=";",
    dtype=str,
    encoding="utf-8"
)

proprietaire = pd.read_csv(
    dossier_ref + r"\sup_proprietaire.txt",
    sep=";",
    dtype=str,
    encoding="utf-8"
)

# Garder une seule fois chaque support
support = support.drop_duplicates(subset="SUP_ID")

# Relier les supports aux noms de leurs proprietaires
fusion = pd.merge(
    support,
    proprietaire,
    on="TPO_ID",
    how="left"
)

# Remplacer les proprietaires inconnus
fusion["TPO_LB"] = fusion["TPO_LB"].fillna("Non renseigne")

# Compter les supports par proprietaire
nombre = fusion["TPO_LB"].value_counts()

print(nombre)

# Afficher les 5 proprietaires les plus representes
nombre.head(5).plot(kind="bar", color="grey")

plt.title("A qui appartiennent les supports ?")
plt.xlabel("Proprietaire")
plt.ylabel("Nombre de supports")
plt.tight_layout()
plt.show()
