# SAE-15--Traiter-des-donn-es
Analyse des installations radioélectriques en France
HOW TO USE

ANTENNA_HEIGHT_ANALYSIS.PY – This program allows you to analyze the height of antenna supports using ANFR data (sup_support.txt and sup_nature.txt). It calculates the average, minimum, and maximum support height. It also compares the average height for each type of support and generates a bar chart to make the results easier to understand.

Installation: pandas, matplotlib

SUP_SUPPORT.TXT – This file contains information about antenna supports, including their heights and support types. It is used as the main data source for the analysis.

SUP_NATURE.TXT – This file contains the names of the different support types. It is used with sup_support.txt to identify and compare the types of supports.

Important: Place the data folders (data and ref) in the same project folder as your Python program. Make sure the file paths are correct before running the code.
