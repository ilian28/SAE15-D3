# SAE-15--Traiter-des-donn-es
Analyse des installations radioélectriques en France
# SAE-15--Traiter-des-donn-es
Analyse des installations radioélectriques en France

## 1- Les Modules nécessaires
Le script utilise trois bibliothèques externes (`pandas`, `matplotlib` et `folium`), en plus de modules déjà inclus dans Python (`pathlib`, `os`, `zipfile`, `webbrowser`).

---

## 2- Organisation des dossiers et des fichiers
Le script doit être dans le dossier `SAE15` (téléchargé à partir du cahier des charges) ; le code utilise `Path("data") / "data"` et `Path("ref") / "ref"`.

```text
SAE15/
├── Code_final_SAE15.py (ou votre notebook .ipynb)
├── data/
│   └── data/
│       ├── sup_station.txt
│       ├── sup_support.txt
│       ├── sup_antenne.txt
│       ├── sup_bande.txt
│       └── sup_emetteur.txt
└── ref/
    └── ref/
        ├── sup_nature.txt
        ├── sup_proprietaire.txt
        ├── sup_exploitant.txt
        └── sup_type_antenne.txt
```

---

## 3- Structure globale du code

Le script regroupe le traitement des données et la restitution visuelle en **5 blocs fonctionnels** suivis de l'affichage des graphiques :

* **Initialisation et chemins d'accès :** import des bibliothèques (`pandas`, `matplotlib.pyplot`, `pathlib.Path`) et définition des chemins `dossier = Path("data") / "data"` et `dossier_ref = Path("ref") / "ref"`.
* **Programme 1 — Types de supports les plus utilisés :** chargement de `sup_station.txt`, `sup_support.txt` et `sup_nature.txt`, dédoublonnage, jointures, calcul du Top 10 et affichage des effectifs et pourcentages.
* **Programme 2 — Propriétaires des supports :** chargement de `sup_proprietaire.txt`, jointure sur `TPO_ID`, gestion des valeurs manquantes (`"Non renseigne"`), décompte et graphique en barres (`plt.bar` via `.plot(kind="bar")`) des 5 premiers propriétaires.
* **Programme 3 — Mutualisation des supports :** chargement de `sup_station.txt` (`latin-1`), jointure sur `STA_NM_ANFR` avec les supports, nettoyage des identifiants manquants (`SUP_ID`, `ADM_ID`), comptage du nombre d'exploitants par support, calcul du taux de mutualisation (`nb >= 2`) et graphique circulaire (`plt.pie`).
* **Programme 4 — Analyse des hauteurs d'antennes :** chargement de `sup_antenne.txt`, conversion numérique de `AER_NB_ALT_BAS`, filtrage des valeurs manquantes et négatives, calcul de la moyenne et de la médiane, et tracé d'un histogramme par tranches de 10 mètres (`0` à `100 m`).
* **Programme 5 — Carte interactive :** conversion des coordonnées DMS en degrés décimaux, classification par `TPO_ID` (couleurs et groupes), création d'une carte `folium` avec fonds OpenStreetMap / OpenTopoMap, repères de villes, `MarkerCluster`, légende HTML, export en `.html` et archive `.zip`, puis ouverture dans le navigateur.

---

## 4- Fichiers produits et dépannage rapide

* **Sorties générées :** `carte_antennes_france.html` et `carte_antennes_france.zip` dans le répertoire courant, en plus des affichages console et graphiques.
* **Erreur `FileNotFoundError` :** vérifiez que le dossier courant est bien `SAE15` et que les sous-dossiers `data/data/` et `ref/ref/` contiennent les fichiers `.txt` attendus.
## 1- Les Modules nécessaires
Le script utilise trois bibliothèques externes (`pandas`, `matplotlib` et `folium`), en plus de modules déjà inclus dans Python (`pathlib`, `os`, `zipfile`, `webbrowser`).

---

## 2- Organisation des dossiers et des fichiers
Le script doit être dans le dossier `SAE15` (téléchargé à partir du cahier des charges) ; le code utilise `Path("data") / "data"` et `Path("ref") / "ref"`.

```text
SAE15/
├── Code_final_SAE15.py (ou votre notebook .ipynb)
├── data/
│   └── data/
│       ├── sup_station.txt
│       ├── sup_support.txt
│       ├── sup_antenne.txt
│       ├── sup_bande.txt
│       └── sup_emetteur.txt
└── ref/
    └── ref/
        ├── sup_nature.txt
        ├── sup_proprietaire.txt
        ├── sup_exploitant.txt
        └── sup_type_antenne.txt

## 3- Structure globale du code

Le script regroupe le traitement des données et la restitution visuelle en 5 blocs fonctionnels suivis de l'affichage des graphiques :

    Initialisation et chemins d'accès : import des bibliothèques (pandas, matplotlib.pyplot, pathlib.Path) et définition des chemins dossier = Path("data") / "data" et dossier_ref = Path("ref") / "ref".

    -Programme 1 — Types de supports les plus utilisés : chargement de sup_station.txt, sup_support.txt et sup_nature.txt, dédoublonnage, jointures, calcul du Top 10 et affichage des effectifs et pourcentages.

    -Programme 2 — Propriétaires des supports : chargement de sup_proprietaire.txt, jointure sur TPO_ID, gestion des valeurs manquantes ("Non renseigne"), décompte et graphique en barres (plt.bar via .plot(kind="bar")) des 5 premiers propriétaires.

    -Programme 3 — Mutualisation des supports : chargement de sup_station.txt (latin-1), jointure sur STA_NM_ANFR avec les supports, nettoyage des identifiants manquants (SUP_ID, ADM_ID), comptage du nombre d'exploitants par support, calcul du taux de mutualisation (nb >= 2) et graphique circulaire (plt.pie).

    -Programme 4 — Analyse des hauteurs d'antennes : chargement de sup_antenne.txt, conversion numérique de AER_NB_ALT_BAS, filtrage des valeurs manquantes et négatives, calcul de la moyenne et de la médiane, et tracé d'un histogramme par tranches de 10 mètres (0 à 100 m).

    -Programme 5 — Carte interactive : conversion des coordonnées DMS en degrés décimaux, classification par TPO_ID (couleurs et groupes), création d'une carte folium avec fonds OpenStreetMap / OpenTopoMap, repères de villes, MarkerCluster, légende HTML, export en .html et archive .zip, puis ouverture dans le navigateur.

## 4- Fichiers produits et dépannage rapide

    -Sorties générées : carte_antennes_france.html et carte_antennes_france.zip dans le répertoire courant, en plus des affichages console et graphiques.

    -Erreur FileNotFoundError : vérifiez que le dossier courant est bien SAE15 et que les sous-dossiers data/data/ et ref/ref/ contiennent les fichiers .txt attendus.
