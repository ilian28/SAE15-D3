import pandas as pd
import matplotlib.pyplot as plt

dossier = "C:/Users/ilian zihoune/Desktop/ECOLE_ILIAN_ZIhoune/SAE 15/data/data/"
dossier_ref = "C:/Users/ilian zihoune/Desktop/ECOLE_ILIAN_ZIhoune/SAE 15/ref/ref/"

# On recupere les fichiers des supports et de leurs proprietaires
support = pd.read_csv(dossier + "sup_support.txt",
                      sep=";", dtype=str, encoding="utf-8")

proprietaire = pd.read_csv(dossier_ref + "sup_proprietaire.txt",
                           sep=";", dtype=str, encoding="utf-8")

# On garde une seule fois chaque support pour ne pas le compter plusieurs fois
support = support.drop_duplicates(subset="SUP_ID")

# On relie les supports aux noms de leurs proprietaires
fusion = pd.merge(support, proprietaire, on="TPO_ID", how="left")

# Si le proprietaire est inconnu, on indique "Non renseigne"
fusion["TPO_LB"] = fusion["TPO_LB"].fillna("Non renseigne")

# On compte le nombre de supports pour chaque proprietaire
nombre = fusion["TPO_LB"].value_counts()

print(nombre)

# On affiche les 5 proprietaires les plus representes dans un graphique
nombre.head(5).plot(kind="bar", color="grey")

plt.title("A qui appartiennent les supports ?")
plt.xlabel("Proprietaire")
plt.ylabel("Nombre de supports")
plt.tight_layout()
plt.show()import pandas as pd
import matplotlib.pyplot as plt

dossier = "C:/Users/ilian zihoune/Desktop/ECOLE_ILIAN_ZIhoune/SAE 15/data/data/"
dossier_ref = "C:/Users/ilian zihoune/Desktop/ECOLE_ILIAN_ZIhoune/SAE 15/ref/ref/"

# On recupere les fichiers des supports et de leurs proprietaires
support = pd.read_csv(dossier + "sup_support.txt",
                      sep=";", dtype=str, encoding="utf-8")

proprietaire = pd.read_csv(dossier_ref + "sup_proprietaire.txt",
                           sep=";", dtype=str, encoding="utf-8")

# On garde une seule fois chaque support pour ne pas le compter plusieurs fois
support = support.drop_duplicates(subset="SUP_ID")

# On relie les supports aux noms de leurs proprietaires
fusion = pd.merge(support, proprietaire, on="TPO_ID", how="left")

# Si le proprietaire est inconnu, on indique "Non renseigne"
fusion["TPO_LB"] = fusion["TPO_LB"].fillna("Non renseigne")

# On compte le nombre de supports pour chaque proprietaire
nombre = fusion["TPO_LB"].value_counts()

print(nombre)

# On affiche les 5 proprietaires les plus representes dans un graphique
nombre.head(5).plot(kind="bar", color="grey")

plt.title("A qui appartiennent les supports ?")
plt.xlabel("Proprietaire")
plt.ylabel("Nombre de supports")
plt.tight_layout()
plt.show()