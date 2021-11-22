from Base_données.DBMongo import get_client_mongodb
import dns
import pymongo
import pandas as pd


class mongo(object):


    client = get_client_mongodb()

    db = client.Tomates_meteo_Centre8
    mycl = db["données"]
    Dat = pd.DataFrame(list(mycl.find()))
    DT = pd.DataFrame(Dat, columns = ['Date', 'prix moyen au kg', 'Production quantité \ntonne(s)', 'Température minimale en °C', 
                              'Température maximale en °C', 'précipitations en mm','Ensoleillement en min', 'Rafales (vitesse du vent) en km/h','catégorie tomates'])
    DT.rename(columns={"Production quantité \ntonne(s)": "Production quantité tonne(s)"},inplace=True)
    DT.to_csv('DATA/TMN.csv',index = False)


    
