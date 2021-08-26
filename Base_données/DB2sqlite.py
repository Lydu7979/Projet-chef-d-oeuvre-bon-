import sqlite3
import pandas as pd



def bdd_sql():
    conn = sqlite3.connect('TM2.db')
    cur = conn.execute("SELECT * FROM mytable")
    rows = cur.fetchall()
    dat3  = pd.read_sql_query("SELECT * FROM mytable", conn)
    
    cur.close()
    conn.close()
    return dat3 









