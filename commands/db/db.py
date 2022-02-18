import sqlite3

connect = sqlite3.connect('commands/db/datas.db')
c = connect.cursor()

def commit():
	connect.commit()

def close():
	connect.close()

def exe(command):
	return c.execute(command)

def exe_many(command,values):
	return c.executemany(command,values)

def fetch_one():
	return c.fetchone()