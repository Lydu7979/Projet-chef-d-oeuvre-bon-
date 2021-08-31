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

def j():
    st.subheader("Choix du nombre de jours pour les prédictions du prix et de la production")
    n = st.slider('Choisir le nombre de jours pour les prédictions:',1,30)
    
    return n



def data_loadTB():
    excel_names = ["./DATA_Fruits/Tomates - Bretagne 2019.xlsx", "./DATA_Fruits/Tomates - Bretagne 2020.xlsx", "./DATA_Fruits/Tomates - Bretagne 2021.xlsx"]
    excels = [pd.ExcelFile(name) for name in excel_names]
    frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
    frames[1:] = [df[1:] for df in frames[1:]]
    combined = pd.concat(frames)
    combined.to_excel("Tomates_Bretagne.xlsx", header=False, index=False)
    TB = pd.read_excel("Tomates_Bretagne.xlsx")
    return TB


def data_vizTB():
    data = data_loadTB()
    data['Date liv.'] = pd.to_datetime(data['Date liv.'],infer_datetime_format=True)
    data.sort_values(by='Date liv.', ascending=True, inplace = True) 
    data = data.set_index(['Date liv.'])

    Prix = data['P.R EUR']
    Production =  data['Quantité U.P']
    scaler = MinMaxScaler()

    data[['prix_n', 'production_n']] = scaler.fit_transform(data[['P.R EUR', 'Quantité U.P']])
    fig = plt.figure(figsize=(10,5))
    plt.plot(data.prix_n, label="prix normalisé", color = 'darkviolet')
    plt.plot(data.production_n, label="production normalisée", color = 'gold')
    plt.title("Représentation du prix et de la production")
    plt.legend(loc="upper right")
    plt.grid(True)
    return	st.pyplot(fig)

def Pred_prixTB():
    mod = pickle.load(open('modèle_ARIMA_Prix2.pkl', 'rb'))
    n = j()
    period = int(n)
    data = data_loadTB()
    Prix = data['P.R EUR']
    forecast,err,ci = mod.forecast(steps= period, alpha = 0.05)
    n_prix = pd.DataFrame({"Date":pd.date_range(start=datetime.date.today(), periods=period, freq='D'), 'prix dans '+ str(n) +" "+'jours' :list(forecast)})
    df_forecast = pd.DataFrame({'Prix dans '+  str(n) +" "+'jours' :forecast},index=pd.date_range(start=datetime.date.today(), periods=period, freq='D'))
    df_forecast.to_csv("Forecast.csv")
    forcast=pd.read_csv('Forecast.csv')	
    forcast.rename(columns={"Unnamed: 0": "Date liv.",'Prix dans '+ str(n) +'jours':"P.R EUR"},inplace=True)
    forcast['Date liv.'] = pd.to_datetime(forcast['Date liv.'],infer_datetime_format=True)
    forcast.index=forcast['Date liv.']
    del forcast['Date liv.']
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



def Pred_proTB():
    mod2 = pickle.load(open('modèle_ARIMA_Production2.pkl', 'rb'))
    n = j()
    period = int(n)
    data = data_loadTB()
    Production =  data['Quantité U.P']
    forecast2,err,ci = mod2.forecast(steps= period, alpha = 0.05)
    df_forecast2 = pd.DataFrame({'Production dans '+ str(n) +" "+'jours' :forecast2},index=pd.date_range(start=datetime.date.today(),periods=period, freq='D'))
    n_pro = pd.DataFrame({"Date liv.":pd.date_range(start=datetime.date.today(), periods=period, freq='D'),'production dans '+ str(n) +" "+'jours' :list(forecast2)})
    df_forecast2.to_csv("Forecast2.csv")
    forcast2=pd.read_csv('Forecast2.csv')
    forcast2.rename(columns={"Unnamed: 0": "Date liv.",'Production dans '+ str(n) +'jours':"Quantité U.P"},inplace=True)
    forcast2.head()
    forcast2['Date liv.'] = pd.to_datetime(forcast2['Date liv.'],infer_datetime_format=True)
    forcast2.index=forcast2['Date liv.']
    del forcast2['Date liv.']
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










