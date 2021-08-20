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
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import pickle
from statsmodels.tsa.arima_model import ARIMAResults
import datetime
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
st.sidebar.info("Une fois connecté(e). vous aurez accès à l'application.")
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
	st.info("Dans un premier temps, vous verrez la base de données (sous forme de tableau) avec les informations. Ensuite, vous pourrez ensuite choisir le nombre de jours, pour les prédicitions.")			
	st.subheader("Base de données Mongodb")
	
	client = get_client_mongodb()

	db = client.Tomates_meteo_Centre5
	mycl = db["donnees"]

	Dat = pd.DataFrame(list(mycl.find()))
	Dat = Dat.drop_duplicates(subset= ['index'])
	
	db2 = client.Tomates_prix_production_Centre
	mycl2 = db2["donnees"]

	Dat2 = pd.DataFrame(list(mycl2.find()))
	Dat2 = Dat2.drop_duplicates(subset= ['index'])
	

	st.dataframe(Dat)
	

	
	#st.dataframe(Dat2)
	#st.info("Ici, vous verrez la base de données avec uniquement la date,le prix, la production et l'id.")



	#st.dataframe(Dat)

	#db2 = client.Tomates_prix_production_Centre
	#mycl2 = db2["donnees"]

	#Dat2 = pd.DataFrame(list(mycl2.find()))
	#Dat2 = Dat2.drop_duplicates(subset= ['index'])
	
	#st.info("Ici, le client a accès à la base de données.")
	#DT = pd.DataFrame(Dat, columns = ['Date', 'prix moyen au kg', 'Production quantité \ntonne(s)', 'Température minimale en °C', 
	#                             'Température maximale en °C', 'précipitations en mm','Ensoleillement en min', 'Rafales (vitesse du vent) en km/h'])
	#DT.to_csv('DATA/TM16.csv',index = False)                              

	#st.write("Base de données concernant le prix et la production")

	#st.dataframe(Dat2)
	#st.info("Contrairement à la première base de données, le client verra uniquement la date, avec le prix, la production et l'id.")

	DATA_URL =('./DATA/TM16.csv')
	
	st.subheader("Choix du nombre de jours pour les prédictions du prix et de la production")
	n = st.slider('Nombre de jours pour les prédictions:',1,30) # n correspond au nombre de jours que l'utilisateur choisira pour les prédictions
	st.info("Ici, vous pourrez choisir le nombre de jours (entre 1 et 30), que vous voulez pour la prédiction du prix et de la production. Pour choisir le nombre de jours, cliquez sur le point rouge , et faites le glisser vers la droite.")
	st.write('le nombre de jours choisis pour les prédictions, est:', n)
	period = int(n)
	
	st.subheader("Représentation graphique des données (prix et production réunis)")

	@st.cache(allow_output_mutation=True)
	def load_data():
		data = pd.read_csv(DATA_URL)
		return data



	#data_load_state = st.text('Téléchargement des données...')
	data = load_data()
	#data_load_state.text('Téléchargement des données... terminé!')



	data['Date'] = pd.to_datetime(data['Date'],infer_datetime_format=True)
	data.sort_values(by='Date', ascending=True, inplace = True) 
	
	data = data.set_index(['Date'])

	data.rename(columns={"Production quantité \ntonne(s)": "Production en tonnes"},inplace=True)
	#data = data.drop(columns=["Unnamed: 0"])
	
	#st.write(data.columns)
	Prix = data['prix moyen au kg']
	Production =  data['Production en tonnes']
				
	scaler = MinMaxScaler()
				
	data[['prix_n', 'production_n']] = scaler.fit_transform(data[['prix moyen au kg', 'Production en tonnes']])
	#st.dataframe(data)

	fig = plt.figure(figsize=(10,5))
	plt.plot(data.prix_n, label="prix normalisé", color = 'darkviolet') # k b r y g m c C0 - C5
	plt.plot(data.production_n, label="production normalisée", color = 'gold')
	
	plt.title("Représentation du prix au kilo et de la production")
	plt.legend(loc="upper right")
	plt.grid(True)
	st.pyplot(fig)
			
	#st.line_chart(Prix)
	st.info("Il s'agit de l'évolution du prix au kilo des tomates, et de la production de tomates, au cours du temps. Il a fallu normaliser le prix et la production car les unités n'étaient pas les mêmes. D'ou les valeurs comprises entre 0 et 1, sur le graphe.")
	st.subheader("Représentation des données séparées")
	st.info("Vous pourrez voir l'évolution au cours du temps de chacune des données. Parmi les données, on retrouve le prix, la production, les données météos(température(minimale et maximale) en °C, précipitations en mm, durée de l'ensoleillement en min, vitesse du vent en km/h).")
	tache = st.selectbox("Données",["prix au kilo","production","Température minimale en °C","Température maximale en °C","précipitations en mm","Durée de l'ensoleillement en min","Vitesse du vent en km/h"])
	
	
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


	#print("*"*20)
	#print(type(data))
	#prix = pd.DataFrame({"prix":list(Prix)})
	#prix.reindex(data['Date'])
	#print(type(data))
	# st.dataframe(data)
	#print("lol")
	#st.bar_chart(Prix)

	#st.line_chart(Production)
	#st.info("Il s'agit de l'évolution du production de tomates en tonnes au cours du temps.")
	# st.dataframe(pd.DataFrame({"production":list(Production)}))

		#modèles
	st.subheader("Prédicition du prix et de la production")
	st.info("Dans cette partie, vous verrez les prédictions du prix en premier et de la production ensuite.")		
			
	mod = pickle.load(open('modèle_ARIMA_Prix2.pkl', 'rb'))
			

	mod2 = pickle.load(open('modèle_ARIMA_Production2.pkl', 'rb'))

	forecast,err,ci = mod.forecast(steps= period, alpha = 0.05)

	df_forecast = pd.DataFrame({'Prix dans '+  str(n) +" "+'jours' :forecast},index=pd.date_range(start=datetime.date.today(), periods=period, freq='D'))
			
	#st.table(df_forecast)
	st.subheader("Prédiction du prix")
	n_prix = pd.DataFrame({"Date":pd.date_range(start=datetime.date.today(), periods=period, freq='D'), 'prix dans '+ str(n) +" "+'jours' :list(forecast)})
	st.dataframe(n_prix)
	st.info("Voici un tableau avec les dates (en commençant par celle d'aujourd'hui), et des prédicitons du prix par rapport aux dates, et au nombre de jours choisis. Ci-dessous, voici la représentation graphique de ces données.")
	df_forecast.to_csv("Forecast.csv")
	st.line_chart(df_forecast)
	
	forcast=pd.read_csv('Forecast.csv')
	
	forcast.rename(columns={"Unnamed: 0": "Date",'Prix dans '+ str(n) +'jours':"prix moyen au kg"},inplace=True)
	forcast['Date'] = pd.to_datetime(forcast['Date'],infer_datetime_format=True)
	forcast.index=forcast['Date']
	del forcast['Date']
	fig1 = pd.concat([Prix,forcast])
	fig3 = plt.figure(figsize=(10,5))
	
	plt.plot(Prix, label="prix (valeurs observées)", color = 'darkviolet')
	plt.plot(forcast, label="prix (valeurs prédites)", color = 'coral')
	plt.title("Représentation du prix avec les données prédites")
	plt.xlabel("Année")
	plt.ylabel("Prix")
	plt.legend(loc="upper right")
	plt.grid(True)
	st.pyplot(fig3)
	st.info("Le tracé en violet représente les données observées, provenant du dataset créé à partir de la base de donnée. Le tracé en orange représente les données prédites par rapport au jour choisi.")




			

	forecast2,err,ci = mod2.forecast(steps= period, alpha = 0.05)
	df_forecast2 = pd.DataFrame({'Production dans '+ str(n) +" "+'jours' :forecast2},index=pd.date_range(start=datetime.date.today(),periods=period, freq='D'))
			
	#st.table(df_forecast2)
	st.subheader("Prédiction de la production")
	n_pro = pd.DataFrame({"Date":pd.date_range(start=datetime.date.today(), periods=period, freq='D'),'production dans '+ str(n) +" "+'jours' :list(forecast2)})
	st.dataframe(n_pro)
	st.info("Voici un tableau avec les dates (en commençant par celle d'aujourd'hui), et des prédicitons de la production par rapport aux dates, et au nombre de jours choisis. Ci-dessous, voici la représentation graphique de ces données.")
	df_forecast2.to_csv("Forecast2.csv")
	st.line_chart(df_forecast2)
	forcast2=pd.read_csv('Forecast2.csv')
	forcast2.rename(columns={"Unnamed: 0": "Date",'Production dans '+ str(n) +'jours':"Production en tonnes"},inplace=True)
	forcast2.head()
	forcast2['Date'] = pd.to_datetime(forcast2['Date'],infer_datetime_format=True)
	forcast2.index=forcast2['Date']
	del forcast2['Date']
	fig2 = pd.concat([Production,forcast2])
	fig4 = plt.figure(figsize=(10,5))
	
	plt.plot(Production, label="production (valeurs observées)", color = 'gold')
	plt.plot(forcast2, label="production (valeurs prédites)", color = 'coral')
	plt.title("Représentation du prix avec les données prédites")
	plt.xlabel("Année")
	plt.ylabel("Production")
	plt.legend(loc="upper right")
	plt.grid(True)
	st.pyplot(fig4)
	st.info("Le tracé en jaune représente les données observées, provenant du dataset créé à partir de la base de donnée. Le tracé en orange représente les données prédites par rapport au jour choisi.")




	



	



	#if st.checkbox('Show forecast data'):
	#	st.subheader('forecast data')
	#	st.dataframe(pd.DataFrame({'prix dans '+ str(n)+'jours' :list(forecast)}))
	#	st.dataframe(pd.DataFrame({'production dans '+ str(n)+'jours' :list(forecast2)}))

	
			
	

			



	#Date = st.date_input('Choisir une date: ')
	#st.info("En cliquant sur l'encadré gris foncé, vous pouvez choisir et cliquer la date que vous souhaitez.")
	#st.write("La date choisie est:", Date)
    
	
	
	




	
		
	#st.write("Représentation du prix avec les données prédites")
	#st.line_chart(fig1)
	#st.info("Le tracé en bleu représente les données observées, provenant du dataset choisi. Le tracé en orange représente les données prédites par rapport au jour choisi.")
		
		# #st.markdown(csv_downloader(fig1), unsafe_allow_html=True)

		#st.write("Représentation de la production avec les données prédites")
		#st.line_chart(fig2)
		#st.info("Le tracé en bleu représente les données observées, provenant du dataset choisi. Le tracé en orange représente les données prédites par rapport au jour choisi.")
		

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