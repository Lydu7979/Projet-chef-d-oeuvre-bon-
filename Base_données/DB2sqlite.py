import sqlite3
import pandas as pd
import hashlib


def bdd_sql():
    conn = sqlite3.connect('data.db')

    dat3  = pd.read_sql_query("SELECT * FROM userstable", conn)
    dat3['pwd'] = dat3['password'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    dat3 = dat3.drop(["password"], axis = 1)
    dat3 = dat3.drop_duplicates()
    dat3 = dat3.rename(index = str, columns = {'pwd':'password'})
    
    conn.close()
    return dat3









