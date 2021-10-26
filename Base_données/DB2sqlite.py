import sqlite3
import pandas as pd
import hashlib


def bdd_sql():
    conn = sqlite3.connect('data.db')

    dat3  = pd.read_sql_query("SELECT * FROM userstable", conn)
    dat3.reset_index(inplace=True)
    dat3 = dat3.rename(index = str, columns = {'index':'id_users'})
    dat3['pwd'] = dat3['password'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    dat3 = dat3.drop(["password"], axis = 1)
    dat3 = dat3.drop_duplicates()
    dat3 = dat3.rename(index = str, columns = {'pwd':'password'})
    dat3.to_csv('Base_données/data_users.csv',index = False)
    dat4 = pd.read_csv('Base_données/data_users.csv') 
    
    conn.close()
    return dat4








