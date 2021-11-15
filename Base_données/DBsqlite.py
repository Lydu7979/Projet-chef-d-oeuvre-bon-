
import sqlite3


#c = co.cursor() 

def create_usertable():
	co = sqlite3.connect("data.db")
	c = co.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT, PRIMARY KEY(username))')
	c.close()


def add_userdata(username,password):
	co = sqlite3.connect("data.db")
	c = co.cursor()
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))

	co.commit()
	c.close()

def login_user(username,password)->list:
	co = sqlite3.connect("data.db")
	c = co.cursor()
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	c.close()
	return data

def view_all_users():
	co = sqlite3.connect("data.db")
	c = co.cursor()
	c.execute('SELECT * FROM usertable')
	data = c.fetchall()
	c.close()
	return data

