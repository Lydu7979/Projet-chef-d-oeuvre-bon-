# Projet-chef-d-oeuvre-bon



L'objectif est de prédire le prix et la production des tomates pour la région Centre-Val-de-Loire, 
en fonction de la météo (pluie, vent, ensoleillement).

# Prerequisites

Installation des librairies fbprophet,et des librairies dédiées au modèle ARIMA.

# ETAPE 1 : Scrapping et DATA preprocessing

- Scrapping des sites internet https://rnm.franceagrimer.fr/prix?TOMATE&12MOIS (pour la production et les prix des tomates. Comme il s’agit de la région Centre Val-de-Loire, les tomates en question sont “TOMATE ronde Val de Loire cat.I 57-67mm colis 10kg” et “TOMATE ronde Val de Loire cat.I 67-82mm colis 10kg”) et https://www.infoclimat.fr/ (pour les données météos provenant de la station météo Orléans Bricy).


- les colones pour le dataset : date, prix, température minimale, température maximale, prépicipitations, ensoleillement, et vitesse du vent. Pour 2 modèles, une colonne a été ajoutée et encodée: la catégorie de tomates. Pour ces mêmes modèles, les dates sont dans une colone, et séparées en jour, mois et années , puis encodées.

- Data visualisation.

# ETAPE 2: Modélisation

4 modèles testés : ARIMA, Prophet, Régression linéaire, et Random Forest.
metrics choisis: RMSE et MAE
Pour les 2 premiers modèles, prédiction du prix et de la production dans 7 jours.

# ETAPE 3: Application

L'application affichera la prédiction du prix et de la production de tomates dans 7 jours, avec le modèle ARIMA et la librairie Streamlit.
