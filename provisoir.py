import sqlite3


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
#Création bases données Mongodb

create_usertable()
user, pwd = "toto", "234"
# add_userdata(user,pwd)
data = login_user(user,pwd)
print(data)