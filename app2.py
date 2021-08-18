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
timestr = time.strftime("%Y%m%d-%H%M%S")
import dns
import logging
from Base_données.DBMongo import get_client_mongodb
from Base_données.DBsqlite import create_usertable, add_userdata, login_user, view_all_users
# from pages.dowload_data import download
logging.basicConfig(filename='demo.log')
logging.debug('This message should go to the log file')

@st.cache
def csv_downloader(data):
	csvfile = data.to_csv()
	b64 = base64.b64encode(csvfile.encode()).decode()
	new_filename = "new_text_file_{}_.csv".format(timestr)
	# st.markdown("#### Télécharger fichier ###")
	href = f'<a href="data:file/csv;base64,{b64}">Cliquer ici!!!</a>'
	return href

#Partie connexion
st.sidebar.subheader("Création compte")
username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type = 'password')

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

	# uploaded_file = st.file_uploader("Télécharger un fichier sous le format csv ou excel.", type = ['csv', 'xlsx'])
	# global data
	# if uploaded_file is not None:
	# 	try:
	# 		data = pd.read_csv(uploaded_file)
	# 	except Exception as e:
	# 		print(e)
	# 		data = pd.read_excel(uploaded_file)

	# 	st.dataframe(data)
	# 	#data.to_csv('DATA/TM14.csv', index=False)
	# 	#Da =
	# 	# tele1 = download(data.to_csv()).tele()
	# 	#st.write(st.__version__)
	# 	st.markdown(csv_downloader(data), unsafe_allow_html=True)
	st.title('App Prix Production de tomates')
	file = 'Tomate.png'
	#image = Image.open(file) 
	st.image(file)
	st.markdown("L'application qui vous aide à prédire le prix de tomates au kilo, et la production dans le futur.")

	st.write("Base de données Mongodb")
	client = get_client_mongodb()

	db = client.Tomates_meteo_Centre5
	mycl = db["donnees"]

	Dat = pd.DataFrame(list(mycl.find()))
	Dat = Dat.drop_duplicates(subset= ['index'])
	st.dataframe(Dat)
	st.markdown("L'application affiche la base de données sous forme de dataframe.")
	st.info("Ici, le client a accès à la base de données.")
	#DT = pd.DataFrame(Dat, columns = ['Date', 'prix moyen au kg', 'Production quantité \ntonne(s)', 'Température minimale en °C', 
	#                             'Température maximale en °C', 'précipitations en mm','Ensoleillement en min', 'Rafales (vitesse du vent) en km/h'])
	#DT.to_csv('DATA/TM15.csv')                              

	st.write("Base de données concernant le prix et la production")

	db2 = client.Tomates_prix_production_Centre
	mycl2 = db2["donnees"]

	Dat2 = pd.DataFrame(list(mycl2.find()))
	Dat2 = Dat2.drop_duplicates(subset= ['index'])
	st.dataframe(Dat2)
	st.info("Contrairement à la première base de données, le client verra uniquement la date, avec le prix, la production et l'id.")




	dataset  = ('TM','TM2','TM3', 'TM4', 'TM5', 'TM6', 'TM7', 'TM8', 'TM9', 'TM10', 'TM11', 'TM12', 'TM13', 'TM14', 'TM15')

	option = st.selectbox('Choisir le dataset pour les prédictions',dataset)
	st.info("Ici, vous pourrez choisir le dataset que vous souhaitez. Le dernier dataset contient les données les plus récentes.")
	DATA_URL =('./DATA/'+option+'.csv')


	n = st.number_input('Mettre le nombre:') # n correspond au nombre de jours que l'utilisateur choisira pour les prédictions
	st.info("Ici, vous pourrez choisir le nombre de jours, que vous voulez pour la prédiction du prix et de la production.")
	st.write('le nombre de jours choisis pour les prédictions, est:', n)
	period = int(n)



	@st.cache(allow_output_mutation=True)
	def load_data():
		data = pd.read_csv(DATA_URL)
		return data



	#data_load_state = st.text('Téléchargement des données...')
	data = load_data()
	#data_load_state.text('Téléchargement des données... terminé!')



	data['Date'] = pd.to_datetime(data['Date'],infer_datetime_format=True)
	data.sort_values(by='Date', ascending=True, inplace = True) 
	# data2 = data[['Date','']]
	data = data.set_index(['Date'])

	Prix = data['prix moyen au kg']
	Production =  data['Production quantité \ntonne(s)']
	print("*"*20)
	st.write("Représentation du prix (en haut) et de la production (en bas)")
	st.line_chart(Prix)
	st.info("Il s'agit de l'évolution du prix au kilo des tomates au cours du temps.")
	print("*"*20)
	print(type(data))
	prix = pd.DataFrame({"prix":list(Prix)})
	#prix.reindex(data['Date'])
	print(type(data))
	# st.dataframe(data)
	print("lol")
	#st.bar_chart(Prix)

	st.line_chart(Production)
	st.info("Il s'agit de l'évolution du production de tomates en tonnes au cours du temps.")
	# st.dataframe(pd.DataFrame({"production":list(Production)}))

#modèles

	mod = ARIMA(Prix,order=(1,0,3))
	results = mod.fit()

	mod2 = ARIMA(Production,order=(1,0,3))
	results2 = mod2.fit()



	Date = st.date_input('Choisir une date (ex: 2021-07-09): ')
	st.info("En cliquant sur l'encadré gris foncé, vous pouvez choisir et cliquer la date que vous souhaitez.")
	st.write("La date choisie est:", Date)



	forecast,err,ci = results.forecast(steps= period, alpha = 0.05)
	df_forecast = pd.DataFrame({'Prix dans '+ str(n) +'jours' :forecast},index=pd.date_range(start=Date, periods=period, freq='D'))
	
	#st.table(df_forecast)
	n_prix = pd.DataFrame({"Date":pd.date_range(start=Date, periods=period, freq='D'), 'prix dans '+ str(n)+'jours' :list(forecast)})
	st.dataframe(n_prix)
	st.info("Vous verrez un tableau avec les dates (en commençant par celle que vous avez choisie), et des prédicitons du prix par rapport aux dates, et au nombre de jours choisis.")
	df_forecast.to_csv("Forecast.csv")
	st.line_chart(df_forecast)
	st.info("Vous verrez une représentation graphique des données présentes dans le tableau ci-dessus.")
	

	forecast2,err,ci = results2.forecast(steps= period, alpha = 0.05)
	df_forecast2 = pd.DataFrame({'Production dans '+ str(n)+'jours' :forecast2},index=pd.date_range(start=Date, periods=period, freq='D'))
	
	#st.table(df_forecast2)
	n_pro = pd.DataFrame({"Date":pd.date_range(start=Date, periods=period, freq='D'),'production dans '+ str(n)+'jours' :list(forecast2)})
	st.dataframe(n_pro)
	st.info("Vous verrez un tableau avec les dates (en commençant par celle que vous avez choisie), et des prédicitons de la production par rapport aux dates, et au nombre de jours choisis.")
	df_forecast2.to_csv("Forecast2.csv")
	st.line_chart(df_forecast2)
	st.info("Vous verrez une représentation graphique des données présentes dans le tableau ci-dessus.")


	#if st.checkbox('Show forecast data'):
	#	st.subheader('forecast data')
	#	st.dataframe(pd.DataFrame({'prix dans '+ str(n)+'jours' :list(forecast)}))
	#	st.dataframe(pd.DataFrame({'production dans '+ str(n)+'jours' :list(forecast2)}))

	forcast=pd.read_csv('Forecast.csv')
	forcast2=pd.read_csv('Forecast2.csv')

	forcast.rename(columns={"Unnamed: 0": "Date",'Prix dans '+ str(n) +'jours':"prix moyen au kg"},inplace=True)
	forcast['Date'] = pd.to_datetime(forcast['Date'],infer_datetime_format=True)
	forcast.index=forcast['Date']
	del forcast['Date']
	#st.line_chart(forcast)
	

	forcast2.rename(columns={"Unnamed: 0": "Date",'Production dans '+ str(n)+'jours':"Production quantité \ntonne(s)"},inplace=True)
	forcast2.head()
	forcast2['Date'] = pd.to_datetime(forcast2['Date'],infer_datetime_format=True)
	forcast2.index=forcast2['Date']
	del forcast2['Date']
	#st.line_chart(forcast2)
	

	fig1 = pd.concat([Prix,forcast])
	fig2 = pd.concat([Production,forcast2])
	
	
	

	st.write("Représentation du prix avec les données prédites")
	st.line_chart(fig1)
	st.info("Le tracé en bleu représente les données observées, provenant du dataset choisi. Le tracé en orange représente les données prédites par rapport au jour choisi.")
	
	# #st.markdown(csv_downloader(fig1), unsafe_allow_html=True)

	st.write("Représentation de la production avec les données prédites")
	st.line_chart(fig2)
	st.info("Le tracé en bleu représente les données observées, provenant du dataset choisi. Le tracé en orange représente les données prédites par rapport au jour choisi.")
	

	# #st.markdown(csv_downloader(fig2), unsafe_allow_html=True)

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