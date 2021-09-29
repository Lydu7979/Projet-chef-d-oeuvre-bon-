
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
from Sécurité.Safe import modi, verif
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
st.sidebar.subheader("Connectez-vous")
username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type = 'password')
ha_pswd = modi(password)
st.sidebar.info("Une fois connecté(e). vous aurez accès à l'application.")
logging.warning("Avant de vous connecter, assurez-vous d'avoir créé votre compte d'utilisateur.")
#Condition pour accéder l'application
@st.cache(suppress_st_warning=True)
def is_well_logged(username, ha_pswd):
	data = login_user(username,verif(password,ha_pswd))
	if data:
		logging.info("Bravo, vous êtes connecté(e) tant que {}. Vous avez accès à l'application.".format(username))
	else:
		logging.error("Nom d'utilisateur/mot de passe incorrect") 
	if data == []:
		return False
	else:
		return True





#Condition pour accéder l'application
S = is_well_logged(username, ha_pswd)
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
	st.title('Application pour prédire le prix et la production de tomates')
	file = 'Tomate.png'
	#image = Image.open(file) 
	st.image(file)
	st.markdown("L'application qui vous aide à prédire le prix de tomates au kilo, et la production dans le futur.")
	logging.info("Bienvenue dans l'application.")			
	st.subheader("Base de données Mongodb")
	
	client = get_client_mongodb()

	db = client.Tomates_meteo_Centre6
	mycl = db["données"]

	Dat = pd.DataFrame(list(mycl.find()))
	Dat = Dat.drop(columns=["index"])
	
	#db2 = client.Tomates_prix_production_Centre
	#mycl2 = db2["donnees"]
	#Dat2 = pd.DataFrame(list(mycl2.find()))
	#Dat2 = Dat2.drop_duplicates(subset= ['index'])

	logging.info("Voici la base de données contenant l'ensemble des données. Pour la voir, appuyez sur le bouton 'Afficher la base de données'")

	if st.button("Afficher la base de données"):
		st.dataframe(Dat)

	#st.subheader("Base de données Sql")

	#st.write(bdd_sql())
	

	
	#st.dataframe(Dat2)
	#st.info("Ici, vous verrez la base de données avec uniquement la date,le prix, la production et l'id.")



	#st.dataframe(Dat)

	#db2 = client.Tomates_prix_production_Centre
	#mycl2 = db2["donnees"]

	#Dat2 = pd.DataFrame(list(mycl2.find()))
	#Dat2 = Dat2.drop_duplicates(subset= ['index'])
	
	#st.info("Ici, le client a accès à la base de données.")
	#DT = pd.DataFrame(Dat, columns = ['Date', 'prix moyen au kg', 'Production quantité \ntonne(s)', 'Température minimale en °C', 
	#                           'Température maximale en °C', 'précipitations en mm','Ensoleillement en min', 'Rafales (vitesse du vent) en km/h'])
	#DT=DT.iloc[pd.to_datetime(DT.Date.astype(str)).argsort()]
	#DT.to_csv('DATA/TM21.csv',index = False)                              

	#st.write("Base de données concernant le prix et la production")

	#st.dataframe(Dat2)
	#st.info("Contrairement à la première base de données, le client verra uniquement la date, avec le prix, la production et l'id.")

	DATA_URL =('./DATA/TM21.csv')
	
	st.subheader("Choix du nombre de jours pour les prédictions du prix et de la production")
	
	n = st.slider('Choisir le nombre de jours pour les prédictions:',1,30) # n correspond au nombre de jours que l'utilisateur choisira pour les prédictions
	logging.info("Ici, vous pourrez choisir le nombre de jours (entre 1 et 30), que vous voulez pour la prédiction du prix et de la production. Pour choisir le nombre de jours, cliquez sur le point rouge , et faites le glisser vers la droite.")
	st.write('le nombre de jours choisis pour les prédictions, est:', n)
	period = int(n)
	
	st.subheader("Représentation graphique des données")
	logging.info('Voici des représentations graphiques des données historiques (les valeurs observées présente dans le dataset créé à partir de la base de données.')

	@st.cache(allow_output_mutation=True)
	def load_data():
		data = pd.read_csv(DATA_URL)
		return data



	#data_load_state = st.text('Téléchargement des données...')
	data = load_data()
	#data_load_state.text('Téléchargement des données... terminé!')



	data['Date'] = pd.to_datetime(data['Date'],infer_datetime_format=True,dayfirst=True)
	data.sort_values(by='Date', ascending=True, inplace = True) 
	
	data = data.set_index(['Date'])

	data.rename(columns={"Production quantité \r\ntonne(s)": "Production en tonnes"},inplace=True)
	#data = data.drop(columns=["Unnamed: 0"])
	#print(data.columns)
	#st.write(data.columns)
	Prix = data['prix moyen au kg']
	Production =  data['Production en tonnes']
				
	scaler = MinMaxScaler()
				
	data[['prix_n', 'production_n']] = scaler.fit_transform(data[['prix moyen au kg', 'Production en tonnes']])
	#st.dataframe(data)

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

		#modèles
	st.subheader("Prédictions du prix et de la production")		
			
	mod = pickle.load(open('modèle_ARIMA_Prix2.pkl', 'rb'))
			

	mod2 = pickle.load(open('modèle_ARIMA_Production2.pkl', 'rb'))

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

	Prédiction = st.radio('Choix entre les prédictions du prix et celles de la production',['Prédiction du prix','Prédiction de la production'])

	#st.table(df_forecast)
	if Prédiction == "Prédiction du prix":		
		choix = st.radio("Choix de la visualisation", ['tableau(valeurs prédites)', 'graphe(valeurs prédites)','graphe(données historiques et données prédites)' ])
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


		if choix == 'graphe(données historiques et données prédites)':
			fig3 = plt.figure(figsize=(10,5))
			plt.plot(Prix, label="prix (valeurs observées)", color = 'darkviolet')
			plt.plot(forcast, label='prix dans '+ str(n) +" "+'jours', color = 'blue')
			plt.title("Représentation du prix avec les données prédites")
			plt.xlabel("Année")
			plt.ylabel("Prix")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig3)
			
			
	if Prédiction == 'Prédiction de la production':
		choix = st.radio("Choix de la visualisation", ['tableau(valeurs prédites)', 'graphe(valeurs prédites)','graphe(données historiques et données prédites)' ])
		if choix == 'tableau(valeurs prédites)':
			st.dataframe(n_pro)

		if choix == 'graphe(valeurs prédites)':
			fig13 = plt.figure(figsize=(10,5))
			plt.plot(forcast2, label='production dans '+ str(n) +" "+'jours', color = 'gold')
			plt.title("Représentation de la production pour les données prédites")
			plt.xlabel("Jour")
			plt.ylabel("Production")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig13)

		if choix == 'graphe(données historiques et données prédites)':
			fig4 = plt.figure(figsize=(10,5))
			plt.plot(Production, label="production (valeurs observées)", color = 'gold')
			plt.plot(forcast2, label='production dans '+ str(n) +" "+'jours', color = 'blue')
			plt.title("Représentation de la production avec les données prédites")
			plt.xlabel("Année")
			plt.ylabel("Production")
			plt.legend(loc="upper right")
			plt.grid(True)
			st.pyplot(fig4)
			


		# #st.markdown(csv_downloader(fig2), unsafe_allow_html=True)

else:
	st.subheader("Créer votre compte")
	n_user = st.text_input("Nom_utilisateur")
	n_pass = st.text_input("Mot_de_passe", type = 'password')
	st.info("Une fois votre nom d'utilisateur et votre mot de passe créés, cliquez sur Nouveau compte.")
	if st.button("Nouveau compte"):
		create_usertable()
		add_userdata(n_user,modi(n_pass))
		st.success("Vous avez créé votre compte.")
		st.info("Connectez-vous dans la partie ou se se trouve la zone 'Connectez-vous'.")
	