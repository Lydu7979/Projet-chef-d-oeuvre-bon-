import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf,pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import warnings                                  
warnings.filterwarnings('ignore')
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import pymongo
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import date
import base64 
import time
timestr = time.strftime("%Y%m%d")
import dns
import logging
from Base_données.DBMongo import get_client_mongodb
from Base_données.DBsqlite import create_usertable, add_userdata, login_user, view_all_users
from Base_données.DB2sqlite import bdd_sql
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import pickle
from statsmodels.tsa.arima_model import ARIMAResults
import datetime
from Tomates_Bretagne.Fruits import j, data_loadTB, data_vizTB, Pred_prixTB, Pred_proTB
from Melon_Poitou.Fruits import j, data_loadMP, data_vizMP, Pred_prixMP, Pred_proMB
from Tomates_Centre.Fruits import j, data_load, Mo, data_vizTC, Pred_prixTC, Pred_proTC


#Partie connexion
st.sidebar.subheader("Connectez-vous")
username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type = 'password')
st.sidebar.info("Une fois connecté(e). vous aurez accès à l'application.")
logging.warning("Avant de vous connecter, assurez-vous d'avoir créé votre compte d'utilisateur.")
#Condition pour accéder l'application
@st.cache
def is_well_logged(username, password):
	data = login_user(username,password)
	if data == []:
		return False
	else:
		return True




#Condition pour accéder l'application
S = is_well_logged(username, password)
if S == True:

    st.title('Application prédiction du prix et de la production de fruits et de légumes')
    st.markdown("L'application qui vous aide à prédire le prix au kilo, et la production dans le futur.")
    logging.info("Bienvenue dans l'application.")

    L_F = st.radio("Choix du fruit ou du légume:", ['Tomate','Melon'])
    if L_F == "Tomate":
        T = st.radio('Choix de la région:', ['Centre','Bretagne'])
        if T == 'Centre':
            st.subheader("Base de données Mongodb")
            if st.button("Afficher la base de données"):
                Mo()
            
            st.subheader('Data Visualisation')
            data_vizTC()

            st.subheader('Prédiction')
            prédiction = "Choix de la prédicition entre le prix et la production:",['Prix','Production']
            if prédiction == "Prix":
                Pred_prixTC()

            if prédiction == "Production":
                Pred_proTC()

        if T == 'Bretagne':
            st.subheader('Data Visualisation')
            data_vizTB()

            st.subheader('Prédiction')
            prédiction = "Choix de la prédicition entre le prix et la production:",['Prix','Production']
            if prédiction == "Prix":
                Pred_prixTB()

            if prédiction == "Production":
                Pred_proTB()

    if L_F == "Melon":
        st.subheader('Data Visualisation')
            data_vizMP()

            st.subheader('Prédiction')
            prédiction = "Choix de la prédicition entre le prix et la production:",['Prix','Production']
            if prédiction == "Prix":
                Pred_prixMP()

            if prédiction == "Production":
                Pred_proMP()

else:
	st.subheader("Créer votre compte")
	n_user = st.text_input("Nom_utilisateur")
	n_pass = st.text_input("Mot_de_passe", type = 'password')
	st.info("Une fois votre nom d'utilisateur et votre mot de passe créés, cliquez sur Nouveau compte.")
	if st.button("Nouveau compte"):
		create_usertable()
		add_userdata(n_user,n_pass)

		st.success("Vous avez créé votre compte.")
		st.info("Connectez-vous, sur la barre de gauche.")








    