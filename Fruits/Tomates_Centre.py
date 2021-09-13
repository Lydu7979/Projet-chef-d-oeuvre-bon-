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

DATA_URL =('./DATA/TM19.csv')

def j():
    st.subheader("Choix du nombre de jours pour les prédictions du prix et de la production")
    n = st.slider('Choisir le nombre de jours pour les prédictions:',1,30)
    
    return n


@st.cache(allow_output_mutation=True)
def load_data():
		data = pd.read_csv(DATA_URL)
		return data

def Mo():
    client = get_client_mongodb()
	db = client.Tomates_meteo_Centre5
	mycl = db["donnees"]
	Dat = pd.DataFrame(list(mycl.find()))
	Dat = Dat.drop_duplicates(subset= ['index'])
	Dat = Dat.drop(columns=["index"])
    logging.info("Voici la base de données contenant l'ensemble des données.")
    DAMDB = st.dataframe(Dat)
    return DAMDB


def data_vizTC():
    data = load_data()
    data['Date'] = pd.to_datetime(data['Date'],infer_datetime_format=True)
	data.sort_values(by='Date', ascending=True, inplace = True) 
	
	data = data.set_index(['Date'])

	data.rename(columns={"Production quantité \ntonne(s)": "Production en tonnes"},inplace=True)
    Prix = data['prix moyen au kg']
	Production =  data['Production en tonnes']
				
	scaler = MinMaxScaler()
				
	data[['prix_n', 'production_n']] = scaler.fit_transform(data[['prix moyen au kg', 'Production en tonnes']])
    action = st.radio('Choix de la représentation graphique',['Représentation graphique des données (prix et production réunis)','Représentation graphique des données séparées'])
	if action == 'Représentation graphique des données (prix et production réunis)':
		fig = plt.figure(figsize=(10,5))
		plt.plot(data.prix_n, label="prix normalisé", color = 'darkviolet')
		plt.plot(data.production_n, label="production normalisée", color = 'gold')
		plt.title("Représentation du prix au kilo et de la production")
		plt.legend(loc="upper right")
		plt.grid(True)
		st.pyplot(fig)
		st.write("Il s'agit de l'évolution du prix au kilo des tomates, et de la production de tomates, au cours du temps. Il a fallu normaliser le prix et la production car les unités n'étaient pas les mêmes. D'ou les valeurs comprises entre 0 et 1, sur le graphe.")
			

	if action == "Représentation graphique des données séparées":
		st.info("Vous pourrez voir l'évolution au cours du temps de chacune des données. Parmi les données, on retrouve le prix, la production, les données météos(température(minimale et maximale) en °C, précipitations en mm, durée de l'ensoleillement en min, vitesse du vent en km/h).")
		tache = st.radio("Choisir les données à visualiser:",["prix au kilo","production","Température minimale en °C","Température maximale en °C","précipitations en mm","Durée de l'ensoleillement en min","Vitesse du vent en km/h"])
		
		if tache == "prix au kilo":
			fig5 = plt.figure(figsize=(10,5))
			plt.plot(Prix, label="prix au kilo", color = 'darkviolet') 
			plt.title("Représentation du prix au kilo au cours du temps")
			plt.xlabel("Année")
			plt.ylabel("Prix")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig5)
		
		if tache == "production":
			fig6 = plt.figure(figsize=(10,5))
			plt.plot(Production, label="production", color = 'gold') 
			plt.title("Représentation de la production au cours du temps")
			plt.xlabel("Année")
			plt.ylabel("Production")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig6)
		
		if tache == "Température minimale en °C":
			fig7 = plt.figure(figsize=(10,5))
			plt.plot(data["Température minimale en °C"], label="Température minimale en °C", color = 'cyan') 
			plt.title("Représentation de la température minimale au cours du temps")
			plt.xlabel("Année")
			plt.ylabel("Température minimale en °C")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig7)
		
		if tache == "Température maximale en °C":
			fig8 = plt.figure(figsize=(10,5))
			plt.plot(data["Température maximale en °C"], label="Température maximale en °C", color = 'magenta') 
			plt.title("Représentation de la température maximale au cours du temps")
			plt.xlabel("Année")
			plt.ylabel("Production")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig8)
		
		if tache == "précipitations en mm":
			fig9 = plt.figure(figsize=(10,5))
			plt.plot(data["précipitations en mm"], label="précipitations en mm", color = 'blue') 
			plt.title("Représentation des précipitations au cours du temps")
			plt.xlabel("Année")
			plt.ylabel("Précipitations en mm")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig9)
		
		if tache == "Durée de l'ensoleillement en min":
			fig10 = plt.figure(figsize=(10,5))
			plt.plot(data["Ensoleillement en min"], label="Ensoleillement en min", color = 'red') 
			plt.title("Représentation de la durée de l'ensoleillement au cours du temps")
			plt.xlabel("Année")
			plt.ylabel("Durée de l'ensoleillement en min")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig10)
		
		if tache == "Vitesse du vent en km/h":
			fig11 = plt.figure(figsize=(10,5))
			plt.plot(data["Rafales (vitesse du vent) en km/h"], label="vitesse du vent en km/h", color = 'green') 
			plt.title("Représentation de la vitesse du vent en km/h au cours du temps")
			plt.xlabel("Année")
			plt.ylabel("Vitesse du vent en km/h")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig11)
    
    return action

def Pred_prixTC():
    mod = pickle.load(open('modèle_ARIMA_Prix2.pkl', 'rb'))
    n = j()
    period = int(n)
    data = load_data()
    data['Date'] = pd.to_datetime(data['Date'],infer_datetime_format=True)
	data.sort_values(by='Date', ascending=True, inplace = True) 
	data = data.set_index(['Date'])
	data.rename(columns={"Production quantité \ntonne(s)": "Production en tonnes"},inplace=True)
    Prix = data['prix moyen au kg']
    forecast,err,ci = mod.forecast(steps= period, alpha = 0.05)
	n_prix = pd.DataFrame({"Date":pd.date_range(start=datetime.date.today(), periods=period, freq='D'), 'prix dans '+ str(n) +" "+'jours' :list(forecast)})
	df_forecast = pd.DataFrame({'Prix dans '+  str(n) +" "+'jours' :forecast},index=pd.date_range(start=datetime.date.today(), periods=period, freq='D'))
	df_forecast.to_csv("Forecast.csv")
	forcast=pd.read_csv('Forecast.csv')	
	forcast.rename(columns={"Unnamed: 0": "Date",'Prix dans '+ str(n) +'jours':"prix moyen au kg"},inplace=True)
	forcast['Date'] = pd.to_datetime(forcast['Date'],infer_datetime_format=True)
	forcast.index=forcast['Date']
	del forcast['Date']
	fig1 = pd.concat([Prix,forcast])
    choix = st.radio("Choix de la visualisation", ['tableau(valeurs prédites)', 'graphe(valeurs prédites)','graphe(données observées et données prédites)' ])
    if choix == 'tableau(valeurs prédites)':
        st.dataframe(n_prix)
		
	if choix == 'graphe(valeurs prédites)':
         fig12 = plt.figure(figsize=(10,5))
         plt.plot(forcast, label='prix dans '+ str(n) +" "+'jours', color = 'darkviolet')
         plt.title("Représentation du prix pour les données prédites")
         plt.xlabel("Jour")
         plt.ylabel("Prix")
         plt.legend(loc="upper right")
         plt.grid(True)
         st.pyplot(fig12)


	if choix == 'graphe(données observées et données prédites)':
         fig3 = plt.figure(figsize=(10,5))
         plt.plot(Prix, label="prix (valeurs observées)", color = 'darkviolet')
         plt.plot(forcast, label='prix dans '+ str(n) +" "+'jours', color = 'coral')
         plt.title("Représentation du prix avec les données prédites")
         plt.xlabel("Année")
         plt.ylabel("Prix")
         plt.legend(loc="upper right")
         plt.grid(True)
         st.pyplot(fig3)

    return choix

def Pred_proTC():
    mod2 = pickle.load(open('modèle_ARIMA_Production2.pkl', 'rb'))
    n = j()
    period = int(n)
    data = load_data()
    data['Date'] = pd.to_datetime(data['Date'],infer_datetime_format=True)
	data.sort_values(by='Date', ascending=True, inplace = True) 
	data = data.set_index(['Date'])
	data.rename(columns={"Production quantité \ntonne(s)": "Production en tonnes"},inplace=True)
    Production =  data['Production en tonnes']
    forecast2,err,ci = mod2.forecast(steps= period, alpha = 0.05)
	df_forecast2 = pd.DataFrame({'Production dans '+ str(n) +" "+'jours' :forecast2},index=pd.date_range(start=datetime.date.today(),periods=period, freq='D'))
	n_pro = pd.DataFrame({"Date":pd.date_range(start=datetime.date.today(), periods=period, freq='D'),'production dans '+ str(n) +" "+'jours' :list(forecast2)})
	df_forecast2.to_csv("Forecast2.csv")
	forcast2=pd.read_csv('Forecast2.csv')
	forcast2.rename(columns={"Unnamed: 0": "Date",'Production dans '+ str(n) +'jours':"Production en tonnes"},inplace=True)
	forcast2.head()
	forcast2['Date'] = pd.to_datetime(forcast2['Date'],infer_datetime_format=True)
	forcast2.index=forcast2['Date']
	del forcast2['Date']
	fig2 = pd.concat([Production,forcast2])
    choix = st.radio("Choix de la visualisation", ['tableau(valeurs prédites)', 'graphe(valeurs prédites)','graphe(données observées et données prédites)' ])
    if choix == 'tableau(valeurs prédites)':
        st.dataframe(n_pro)
		
	if choix == 'graphe(valeurs prédites)':
         fig12 = plt.figure(figsize=(10,5))
         plt.plot(forcast2, label='production dans '+ str(n) +" "+'jours', color = 'gold')
         plt.title("Représentation de la production pour les données prédites")
         plt.xlabel("Jour")
         plt.ylabel("Production")
         plt.legend(loc="upper right")
         plt.grid(True)
         st.pyplot(fig12)


	if choix == 'graphe(données observées et données prédites)':
         fig3 = plt.figure(figsize=(10,5))
         plt.plot(Production, label="production (valeurs observées)", color = 'gold')
         plt.plot(forcast2, label='production dans '+ str(n) +" "+'jours', color = 'coral')
         plt.title("Représentation de la production avec les données prédites")
         plt.xlabel("Année")
         plt.ylabel("Production")
         plt.legend(loc="upper right")
         plt.grid(True)
         st.pyplot(fig3)

    return choix