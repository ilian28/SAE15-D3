import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Chemins des fichiers
dossier = Path("data")/"data"
dossier_ref = Path("ref")/"ref"


# PROGRAMME 1 : LES TYPES DE SUPPORTS LES PLUS UTILISES

# On recupere les fichiers
stations = pd.read_csv(dossier / "sup_station.txt", sep=";", dtype=str, encoding="utf-8")
supports = pd.read_csv(dossier / "sup_support.txt", sep=";", dtype=str, encoding="utf-8")
nature = pd.read_csv(dossier_ref / "sup_nature.txt", sep=";", dtype=str, encoding="utf-8")


# 1. Évite les doublons sur les stations si une colonne identifiant de station existe
for col_sta in ["STA_NM_ANFR", "STA_ID"]:
    if col_sta in stations.columns:
        stations = stations.drop_duplicates(subset=col_sta).copy()

# 2. Évite les doublons sur les supports si SUP_ID existe
if "SUP_ID" in supports.columns:
    supports = supports.drop_duplicates(subset="SUP_ID").copy()

supports_uniques = supports.copy()
    
# 3. Recherche une colonne commune entre stations et supports
colonnes_communes = [c for c in stations.columns if c in supports.columns] 

if not colonnes_communes:
    print("\nAucune colonne commune directe entre sup_station et sup_support.")
    print("Colle les 3 listes de colonnes affichées au-dessus pour qu'on voie la bonne liaison.")
else:  # Cas où au moins une colonne commune existe
    cle_jointure = colonnes_communes[0]
    print(f"\nJointure effectuée sur : {cle_jointure}")

    df = stations.merge(supports, on=cle_jointure, how="left")

    # Évite aussi les doublons après jointure si nécessaire
    df = df.drop_duplicates().copy()

  # Vérifie si NAT_ID est présent des deux côtés pour joindre la nature
    if "NAT_ID" in df.columns and "NAT_ID" in nature.columns:
        df = df.merge(nature, on="NAT_ID", how="left")

  # Récupère les colonnes de nature autres que l'identifiant NAT_ID
    cols_nom = [c for c in nature.columns if c != "NAT_ID"]
    col_nom = cols_nom[-1] if cols_nom else cle_jointure

  # Calcule le nombre total de lignes/enregistrements dans le tableau final
    total = len(df)
    top10 = df[col_nom].fillna("Non renseigné").value_counts().head(10)
    print(f"\nTotal : {total}")
    print("\nTop 10 :")
    for rang, (nom_support, nb) in enumerate(top10.items(), start=1):
        pct = nb / total * 100
        print(f"{rang}. {nom_support} : {nb} ({pct:.1f} %)")


# PROGRAMME 2 : A QUI APPARTIENNENT LES SUPPORTS ?

# On recupere le fichier des proprietaires
proprietaire = pd.read_csv(dossier_ref / "sup_proprietaire.txt",
                           sep=";", dtype=str, encoding="utf-8")

# On relie chaque support a son proprietaire
fusion_proprietaire = pd.merge(supports_uniques, proprietaire,
                              on="TPO_ID", how="left")

# On remplace les proprietaires inconnus
fusion_proprietaire["TPO_LB"] = fusion_proprietaire["TPO_LB"].fillna("Non renseigne")

# On compte les supports pour chaque proprietaire
nombre = fusion_proprietaire["TPO_LB"].value_counts()

print(nombre)

# Graphique
plt.figure(figsize=(10, 6))
nombre.head(5).plot(kind="bar", color="grey")

plt.title("A qui appartiennent les supports ?")
plt.xlabel("Proprietaire")
plt.ylabel("Nombre de supports")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()


# PROGRAMME 3 : LES SUPPORTS SONT-ILS MUTUALISES ?

# On recupere le fichier des installations
station = pd.read_csv(dossier / "sup_station.txt",
                      sep=";", dtype=str, encoding="latin-1")

# On relie les supports aux installations
fusion = pd.merge(supports, station, on="STA_NM_ANFR")

# On retire les identifiants manquants et les doublons
fusion = fusion.dropna(subset=["SUP_ID", "ADM_ID"])
fusion = fusion.drop_duplicates(subset=["SUP_ID", "ADM_ID"])

# On compte le nombre d'exploitants par support
exploitants = fusion["SUP_ID"].value_counts()

mutualises = 0
non_mutualises = 0

# On regarde si chaque support accueille plusieurs exploitants
for nb in exploitants:

    if nb >= 2:
        mutualises = mutualises + 1
    else:
        non_mutualises = non_mutualises + 1

# Calcul des resultats
total = mutualises + non_mutualises
pourcentage_mutualisation = mutualises / total * 100

print("Nombre total de supports :", total)
print("Supports mutualises :", mutualises)
print("Supports non mutualises :", non_mutualises)
print("Pourcentage :", round(pourcentage_mutualisation, 2), "%")

# Graphique
plt.figure(figsize=(8, 6))

plt.pie([mutualises, non_mutualises],
        labels=["Mutualises", "Non mutualises"],
        autopct="%1.1f%%")

plt.title("Les supports sont-ils mutualises ?")

# PROGRAMME 4 : ANALYSE DES HAUTEURS

# On recupere le fichier des antennes
antenne = pd.read_csv(dossier / "sup_antenne.txt",
                      sep=";", dtype=str, encoding="utf-8")

# On transforme les hauteurs en nombres
hauteurs = pd.to_numeric(antenne["AER_NB_ALT_BAS"], errors="coerce")

# On enleve les valeurs manquantes et negatives
hauteurs = hauteurs.dropna()
hauteurs = hauteurs[hauteurs >= 0]

# On calcule la moyenne et la mediane
moyenne = hauteurs.mean()
mediane = hauteurs.median()

print("Hauteur moyenne :", round(moyenne, 2), "m")
print("Hauteur mediane :", round(mediane, 2), "m")

# On cree un graphique par tranche de 10 metres
plt.figure(figsize=(10, 6))
plt.hist(hauteurs, bins=range(0, 101, 10),
         color="grey", edgecolor="black")
plt.title("A quelle hauteur place-t-on les antennes ?")
plt.xlabel("Hauteur des antennes (m)")
plt.ylabel("Nombre d'antennes")
plt.xticks(range(0, 101, 10))
plt.tight_layout()


# PROGRAMME 5 : CARTE INTERACTIVE

import os  # Pour gérer les chemins de fichiers et vérifier s'ils existent
import zipfile  # Pour créer une archive compressée (.zip) de la carte HTML
import folium  # Pour créer la carte interactive
from folium.plugins import MarkerCluster  # Pour regrouper les antennes en clusters (plus fluide et lisible)
import pandas as pd  # Pour charger et nettoyer les données tabulaires
import webbrowser  # Pour ouvrir la carte HTML dans le navigateur
from pathlib import Path


def charger_donnees(chemin_fichier, limite=None):
  """Charge le fichier et convertit les coordonnées DMS en degrés décimaux."""
  print("Chargement et nettoyage des données...")  # Message de suivi dans la console
  df = pd.read_csv(chemin_fichier, sep=";", low_memory=False)  # Lit le fichier séparé par des points-virgules

  # --- Conversion de la latitude (Degrés, Minutes, Secondes -> degrés décimaux) ---
  deg_lat = pd.to_numeric(df["COR_NB_DG_LAT"], errors="coerce")  # Convertit les degrés en nombres (NaN si invalide)
  min_lat = pd.to_numeric(df["COR_NB_MN_LAT"], errors="coerce")  # Convertit les minutes en nombres
  sec_lat = pd.to_numeric(df["COR_NB_SC_LAT"], errors="coerce")  # Convertit les secondes en nombres
  lat = deg_lat + min_lat / 60.0 + sec_lat / 3600.0  # Formule de conversion DMS vers décimal
  lat = lat.where(df["COR_CD_NS_LAT"] != "S", -lat).round(5)  # Rend la latitude négative si au Sud ('S') et arrondit à 5 décimales

  # --- Conversion de la longitude (Degrés, Minutes, Secondes -> degrés décimaux) ---
  deg_lon = pd.to_numeric(df["COR_NB_DG_LON"], errors="coerce")  # Convertit les degrés de longitude en nombres
  min_lon = pd.to_numeric(df["COR_NB_MN_LON"], errors="coerce")  # Convertit les minutes de longitude en nombres
  sec_lon = pd.to_numeric(df["COR_NB_SC_LON"], errors="coerce")  # Convertit les secondes de longitude en nombres
  lon = deg_lon + min_lon / 60.0 + sec_lon / 3600.0  # Formule de conversion DMS vers décimal
  lon = lon.where(df["COR_CD_EW_LON"] != "W", -lon).round(5)  # Rend la longitude négative si à l'Ouest ('W') et arrondit à 5 décimales

  df["LAT"] = lat  # Ajoute la colonne latitude décimale au tableau
  df["LON"] = lon  # Ajoute la colonne longitude décimale au tableau
  df = df.dropna(subset=["LAT", "LON"])  # Supprime les lignes qui n'ont pas de coordonnées valides

  if limite is not None:  # Si une limite est précisée (ex: 10000)
    df = df.head(limite)  # Garde seulement les 'limite' premières lignes

  return df  # Renvoie le tableau nettoyé


def classifier_antenne(val):
  """Retourne (couleur, groupe_filtre, libelle_detaille) selon le code TPO_ID."""
  if pd.isna(val):  # Si le code TPO_ID est vide / manquant
    return "#111111", "multi", "Multi / TPO non renseigné"  # Couleur noire, groupe 'multi', libellé explicite
  try:
    tpo = int(float(val))  # Convertit par exemple "74.0" ou 74.0 en entier 74
  except Exception:
    return "#111111", "multi", f"Multi / TPO ({val})"  # Si la conversion échoue, classe en Multi / Autre

  if tpo == 74:  # Code associé à Orange
    return "#ff8c00", "orange", "Orange (TPO 74)"  # Orange
  elif tpo == 32:  # Code associé à SFR
    return "#e11d48", "sfr", "SFR (TPO 32)"  # Rouge
  elif tpo == 29:  # Code associé à Free Mobile
    return "#7c2d12", "free", "Free Mobile (TPO 29)"  # Marron
  elif tpo == 72:  # Code associé à Bouygues Telecom
    return "#2563eb", "bouygues", "Bouygues Telecom (TPO 72)"  # Bleu
  else:  # Tous les autres codes TPO_ID
    return "#111111", "multi", f"Multi / Autre (TPO {tpo})"  # Noir avec le numéro TPO affiché


def creer_carte(df):
  """Crée une carte libre de droits (OpenStreetMap / OpenTopoMap) avec

  antennes bien visibles, regroupées, filtrables et légendées.
  """
  carte = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles=None)  # Crée la carte centrée sur la France (zoom 6), sans fond par défaut

  # 1. OpenStreetMap (ODbL - libre de droits, sans clé API)
  folium.TileLayer(
      tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",  # URL des tuiles OpenStreetMap
      attr="&copy; OpenStreetMap contributors",  # Mention obligatoire de la source
      name="OpenStreetMap (ODbL)",  # Nom affiché dans le sélecteur de couches
      user_agent="SAE15_Antennes_France/1.0",  # Identifiant de requête pour éviter certains blocages 403
      max_zoom=19,  # Niveau de zoom maximum autorisé
  ).add_to(carte)  # Ajoute cette couche à la carte

  # 2. OpenTopoMap (CC-BY-SA - libre de droits, sans clé API)
  folium.TileLayer(
      tiles="https://tile.opentopomap.org/{z}/{x}/{y}.png",  # URL des tuiles topographiques OpenTopoMap
      attr=(
          "&copy; OpenStreetMap contributors, SRTM | Map style: &copy;"
          " OpenTopoMap (CC-BY-SA)"
      ),  # Mention de licence CC-BY-SA
      name="OpenTopoMap (CC-BY-SA)",  # Nom dans le sélecteur de couches
      max_zoom=17,  # Zoom maximum pour OpenTopoMap
  ).add_to(carte)  # Ajoute cette seconde couche à la carte

  # Liste des grandes villes françaises pour repère visuel (nom, latitude, longitude)
  villes = [
      ("Paris", 48.8566, 2.3522),
      ("Lyon", 45.7640, 4.8357),
      ("Marseille", 43.2965, 5.3698),
      ("Toulouse", 43.6047, 1.4442),
      ("Bordeaux", 44.8378, -0.5792),
      ("Lille", 50.6292, 3.0573),
      ("Nantes", 47.2184, -1.5536),
      ("Strasbourg", 48.5734, 7.7521),
  ]
  for nom, lat, lon in villes:  # Parcourt chaque ville
    folium.Marker(
        location=[lat, lon],  # Position de la ville
        icon=folium.DivIcon(
            html=(
                f'<div style="font-size:11px;font-weight:bold;color:#222;'
                f"background:rgba(255,255,255,0.88);padding:2px 5px;"
                f'border-radius:3px;border:1px solid #888;">{nom}</div>'
            )  # Petite étiquette texte lisible sur la carte
        ),
    ).add_to(carte)  # Ajoute l'étiquette à la carte

  # Configuration des groupes d'opérateurs pour créer un cluster par catégorie
  groupes_config = {
      "bouygues": ("Bouygues Telecom", "#2563eb"),
      "orange": ("Orange", "#ff8c00"),
      "sfr": ("SFR", "#e11d48"),
      "free": ("Free Mobile", "#7c2d12"),
      "multi": ("Multi / Autre", "#111111"),
  }

  clusters_par_groupe = {}  # Dictionnaire pour stocker un MarkerCluster par catégorie
  for cle, (nom_grp, _) in groupes_config.items():  # Pour chaque opérateur / catégorie
    mc = MarkerCluster(name=nom_grp, show=True)  # Crée un cluster visible par défaut
    mc.add_to(carte)  # Ajoute le cluster à la carte
    clusters_par_groupe[cle] = mc  # Enregistre le cluster sous sa clé

  folium.LayerControl(position="bottomright", collapsed=False).add_to(carte)  # Ajoute le panneau de couches/filtres en bas à droite, déplié

  print(f"Ajout de {len(df)} antennes sur la carte...")  # Affiche le nombre total d'antennes traitées
  for row in df.itertuples(index=False):  # Parcourt rapidement chaque ligne du DataFrame
    tpo_raw = getattr(row, "TPO_ID", None)  # Récupère TPO_ID si présent
    color, groupe, libelle = classifier_antenne(tpo_raw)  # Détermine la couleur, le groupe et le libellé détaillé
    sup_id = getattr(row, "SUP_ID", "N/C")  # Récupère l'identifiant du support (ou 'N/C')
    com_insee = getattr(row, "COM_CD_INSEE", "N/C")  # Récupère le code INSEE de la commune (ou 'N/C')
    tpo_txt = "N/C" if pd.isna(tpo_raw) else str(int(float(tpo_raw)))  # Formate le code TPO_ID brut pour l'affichage

    popup_html = (
        f"<b>Support :</b> {sup_id}<br>"
        f"<b>Commune :</b> {com_insee}<br>"
        f"<b>Catégorie :</b> {libelle}<br>"
        f"<b>Code TPO_ID :</b> {tpo_txt}"
    )  # Contenu HTML de la fenêtre pop-up au clic sur une antenne

    # Points agrandis (radius=7) avec contour blanc bien visible sur la carte
    folium.CircleMarker(
        location=[float(row.LAT), float(row.LON)],  # Coordonnées de l'antenne
        radius=7,  # Taille du cercle
        color="#ffffff",  # Contour blanc pour ressortir sur le fond de carte
        weight=1.5,  # Épaisseur du contour
        fill=True,  # Remplit l'intérieur du cercle
        fill_color=color,  # Couleur associée à la catégorie
        fill_opacity=0.9,  # Opacité du remplissage
        popup=folium.Popup(popup_html, max_width=260),  # Associe la pop-up au point
    ).add_to(clusters_par_groupe[groupe])  # Ajoute le point dans le cluster correspondant à son groupe

  # Code HTML/CSS de la légende fixe en bas à gauche
  legende_html = """
    <div style="
        position:fixed;bottom:35px;left:20px;width:235px;
        background:#fff;z-index:9999;font-size:13px;
        border:2px solid #777;border-radius:6px;padding:10px;
        box-shadow:0 0 12px rgba(0,0,0,0.2);">
        <b>Légende - Opérateurs</b><br><br>
        <i style="background:#2563eb;width:12px;height:12px;float:left;margin-right:8px;border-radius:50%;margin-top:3px;border:1px solid #333;"></i> Bouygues Telecom<br>
        <i style="background:#ff8c00;width:12px;height:12px;float:left;margin-right:8px;border-radius:50%;margin-top:3px;border:1px solid #333;"></i> Orange<br>
        <i style="background:#e11d48;width:12px;height:12px;float:left;margin-right:8px;border-radius:50%;margin-top:3px;border:1px solid #333;"></i> SFR<br>
        <i style="background:#7c2d12;width:12px;height:12px;float:left;margin-right:8px;border-radius:50%;margin-top:3px;border:1px solid #333;"></i> Free Mobile<br>
        <i style="background:#111111;width:12px;height:12px;float:left;margin-right:8px;border-radius:50%;margin-top:3px;border:1px solid #333;"></i> Multi / Autre (détail au clic)<br>
    </div>
    """
  carte.get_root().html.add_child(folium.Element(legende_html))  # Injecte la légende dans la page HTML de la carte
  return carte  # Renvoie l'objet carte complet


def compresser_zip(fichier_html):
  """Crée une archive ZIP compressée à côté du fichier HTML."""
  fichier_zip = os.path.splitext(fichier_html)[0] + ".zip"  # Remplace l'extension .html par .zip
  with zipfile.ZipFile(
      fichier_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
  ) as zf:  # Ouvre l'archive ZIP en écriture avec compression maximale (niveau 9)
    zf.write(fichier_html, arcname=os.path.basename(fichier_html))  # Ajoute le fichier HTML dans l'archive
  taille_mo = os.path.getsize(fichier_zip) / (1024 * 1024)  # Calcule la taille du fichier ZIP en mégaoctets (Mo)
  print(f"Archive compressée créée : {fichier_zip} ({taille_mo:.2f} Mo)")  # Affiche le chemin et la taille du ZIP


# --- EXÉCUTION PRINCIPALE ---
chemin = dossier / "sup_support.txt"  # Chemin du fichier source des supports
sortie_html = "carte_antennes_france.html"  # Chemin du fichier HTML de sortie

if os.path.exists(chemin):  # Vérifie que le fichier source existe bien
  df_antennes = charger_donnees(chemin, limite=None)  # Charge et nettoie toutes les antennes (limite=None)
  ma_carte = creer_carte(df_antennes)  # Génère la carte interactive
  ma_carte.save(sortie_html)  # Sauvegarde la carte en fichier HTML
  compresser_zip(sortie_html)  # Compresse le fichier HTML en archive ZIP
  print(f"Carte enregistrée dans : {sortie_html}")  # Confirme l'enregistrement
  webbrowser.open(Path(sortie_html).resolve().as_uri())  # Ouvre la carte dans le navigateur
else:
  print(f"Erreur : Fichier introuvable à l'emplacement {chemin}")  # Message d'erreur


# AFFICHAGE DE TOUS LES GRAPHIQUES

plt.show()