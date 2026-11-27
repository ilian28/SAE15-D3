# SAE-15--Traiter-des-donn-es
Analyse des installations radioélectriques en France

HOW TO USE

- GENERETATE_MAP.IPYNB (SAE15) -
This module allows you to load antenna support data (`sup_support.txt`), convert DMS coordinates into decimal degrees, classify antennas by operator (`TPO_ID`), and generate an interactive map usable in **Jupyter Notebook** and in a **web browser**, accompanied by a compressed `.zip` archive.
Remember to specify the right path, where your html map is located, as well as the path to your source file.

Installation :
pandas
folium

- CARTE_ANTENNES_FRANCE.ZIP -
a map in HTML format, compressed to facilitate data reception; works with the 'generate_map.ipynb' file.
