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
import dns
import logging

logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')
from PIL import Image

st.title('App Prix Production de tomates')
st.markdown("L'application qui vous aide à prédire le prix de tomates au kilo, et la production dans le futur.")

file = 'Tomate.png'
#image = Image.open(file) 
st.image(file)
st.info('Pour accéder aux différentes zones, aller dans le menu situé à gauche du Titre.')


menu = ["Accueil", "Login", "Création compte"]
Choix = st.sidebar.selectbox("Menu",menu)

co = sqlite3.connect("data.db")
c = co.cursor()

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	co.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
  c.execute('SELECT * FROM usertable')
  data = c.fetchall()
  return data

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

if Choix == "Accueil":
    st.subheader("Accueil")
    st.write("Bienvenue dans l'accueil de l'application.")
    st.info("Pour créer votre compte , allez dans la zone 'Création compte'.")
    st.info("Une fois votre compte créé, allez dans la zone 'Login', pour vous connecter.")

elif Choix == "Login":
    st.subheader("Section du Login")

    user_nom = st.sidebar.text_input("Nom d'utilisateur")
    password = st.sidebar.text_input("Mot de passe", type = 'password')

    if st.button("Login"):
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(user_nom,check_hashes(password,hashed_pswd))
        st.success("Connecté(e) en tant que {}".format(user_nom))

        tache = st.selectbox("Tâche",["Base de données","Analyse","Profils"])

        if tache == "Base de données":
            st.subheader("Base de données")
            st.write("Bienvenue dans la page consacrée aux bases de données.")

            st.write("Base de données Mongodb")
            user_name = "Thmo89"
            psw = "Authentication "
            uri2 = "mongodb+srv://{}:{}@cluster1.mknx2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(user_name, psw)

            client = pymongo.MongoClient(uri2)

            db = client.Tomates_meteo_Centre5
            mycl = db["donnees"]

            Dat = pd.DataFrame(list(mycl.find()))
            st.dataframe(Dat)
            st.markdown("L'application affiche la base de données sous forme de dataframe.")

            st.write("Base de données concernant le prix et la production")

            db2 = client.Tomates_prix_production_Centre
            mycl2 = db2["donnees"]

            Dat2 = pd.DataFrame(list(mycl2.find()))
            st.dataframe(Dat2)

            #st.write("pour ajouter des données aux bases existantes, veuillez suivre la démarche ci-dessous.")
            #st.info("Pour les données météo demandées, consulter le site 'https://www.infoclimat.fr', (ex:https://www.infoclimat.fr/climatologie/annee/2012/orleans-bricy/valeurs/07249.html), ensuiter cliquer le jour que vous souhaitez.")
            #i = st.number_input('Mettre le nombre (pensez à bien voir le dernier élément de la colonne "index", en faisant glisser le curseur situé sur le dataframe vers la droite.):')
            #dt = st.text_input("écrivez sous le format suivant (ex: 16/08/21): ")
            #pm = st.number_input("écrivez le prix moyen au kilo, que vous proposez:")
            #pt = st.number_input("écrivez la production en tonnes, que vous proposez:")
            #tmi = st.number_input("écrivez la tempéraure minimale:")
            #tma = st.number_input("écrivez la température maximale:")
            #pem = st.number_input("écrivez les précipitations en mm:")
            #h = st.number_input("écrivez le nombre d'heures entre O et 23:")
            #mi = st.number_input("écrivez le nombre de minutes entre 0 et 59:")
            #v = st.number_input("écrivez la vitesse:")

            #document17 = {"index": int(i), "Date": str(dt), "prix moyen au kg": int(pm), "Production quantité \ntonne(s)" : int(pt), "Température minimale en °C" : int(tmi), "Température maximale en °C" : int(tma), "précipitations en mm" : int(pem), "Ensoleillement en min" : (60 * int(h)) + int(mi) , "Rafales (vitesse du vent) en km/h": int(v)}
            #mycl.insert_one(document17)

            #st.write("première base de données avec l'ajout")
            #st.dataframe(Dat)

            #document1 = {"index": int(i), "Date": str(dt), "prix moyen au kg": int(pm), "Production quantité \ntonne(s)" : int(pt)}
            #mycl2.insert_one(document1)

            #st.write("deuxième base de données avec l'ajout")
            #st.dataframe(Dat2)


        if tache == "Analyse":
            st.subheader("Analyse")
            st.write("Ici, vous pourrez voir des prédictions de prix et de production en fonction du nombre de jour et de la date que vous aurez choisi.")
            
            dataset = ('TM','TM2','TM3', 'TM4', 'TM5', 'TM6', 'TM7', 'TM8', 'TM9', 'TM10', 'TM11', 'TM12')
            option = st.selectbox('Choisir le dataset pour les prédictions',dataset)
            DATA_URL =('./DATA/'+option+'.csv')

            n = st.number_input('écrivez un nombre:') # n correspond au nombre de jours que l'utilisateur choisira pour les prédictions
            st.write('le nombre choisi est:', n)
            period = int(n)

            @st.cache(allow_output_mutation=True)
            def load_data():
                data = pd.read_csv(DATA_URL)
                return data

            data_load_state = st.text('Téléchargement des données...')
            data = load_data()
            data_load_state.text('Téléchargement des données... terminé!')

            data['Date'] = pd.to_datetime(data['Date'],infer_datetime_format=True)
            data.sort_values(by='Date', ascending=True, inplace = True) 
            data = data.set_index(['Date'])

            Prix = data['prix moyen au kg']
            Production =  data['Production quantité \ntonne(s)']

            st.write("Représentation du prix (en haut) et de la production (en bas)")
            st.dataframe(Prix)
            st.dataframe(Production)

            mod = ARIMA(Prix,order=(1,0,3))
            results = mod.fit()

            mod2 = ARIMA(Production,order=(1,0,3))
            results2 = mod2.fit()

            Date = st.date_input('Insérer une date (ex: 2021-07-09): ')
            st.write("La date choisie est:", Date)

            forecast,err,ci = results.forecast(steps= period, alpha = 0.05)
            df_forecast = pd.DataFrame({'Prix dans '+ str(n) +'jours' :forecast},index=pd.date_range(start=Date, periods=period, freq='D'))
            st.write("Prédiction du prix")
            st.table(df_forecast)
            df_forecast.to_csv("Forecast.csv")
            st.line_chart(df_forecast)

            forecast2,err,ci = results2.forecast(steps= period, alpha = 0.05)
            df_forecast2 = pd.DataFrame({'Production dans '+ str(n)+'jours' :forecast2},index=pd.date_range(start=Date, periods=period, freq='D'))
            st.write("Prédiction de la production")
            st.table(df_forecast2)
            df_forecast2.to_csv("Forecast2.csv")
            st.line_chart(df_forecast2)

            if st.checkbox('Show forecast data'):
                st.subheader('forecast data')
                st.write(df_forecast)
                st.write(df_forecast2)

            forcast=pd.read_csv('Forecast.csv')
            forcast2=pd.read_csv('Forecast2.csv')

            forcast.rename(columns={"Unnamed: 0": "Date",'Prix dans '+ str(n) +'jours':"prix moyen au kg"},inplace=True)
            forcast['Date'] = pd.to_datetime(forcast['Date'],infer_datetime_format=True)
            forcast.index=forcast['Date']
            del forcast['Date']
    
            forcast2.rename(columns={"Unnamed: 0": "Date",'Production dans '+ str(n)+'jours':"Production quantité \ntonne(s)"},inplace=True)
            forcast2.head()
            forcast2['Date'] = pd.to_datetime(forcast2['Date'],infer_datetime_format=True)
            forcast2.index=forcast2['Date']
            del forcast2['Date']
    
            fig1 = pd.concat([Prix,forcast])
            fig2 = pd.concat([Production,forcast2])

            st.write("Représentation du prix avec les données prédites")
            st.line_chart(fig1)

            st.write("Représentation de la production avec les données prédites")
            st.line_chart(fig2)

        elif tache == "Profils":
            st.subheader("Profils des utilisateurs")
            user_re = view_all_users()
            cdb = pd.Dataframe(user_re,columns = ["Utilisateur","Mot de passe"])
            db3 = client.Users
            mycl3 = db3["donnees_utilisateurs"]
            cdb.reset_index(inplace=True)
            data_dict = cdb.to_dict("records")
            mycl3.insert_many(data_dict)
            Dat3 = pd.DataFrame(list(mycl3.find()))
            st.write("Base de données utilisateurs")
            st.dataframe(Dat3)    


elif Choix == "Création compte":
    st.subheader("Créer votre compte")
    n_user = st.text_input("Nom d'utilisateur")
    n_pass = st.text_input("Mot de passe", type = 'password')
  
    if st.button("Nouveau compte"):
        create_usertable()
        add_userdata(n_user,n_pass)

        st.success("Vous avez créé votre compte.")
        st.info("Accéder à la section Login dans le menu, pour vous connecter.")




