import sqlite3 as sq

def Auth(username, password):
	conn = sq.connect('db.sqlite')
	cursor = conn.cursor()
	sql = "SELECT * FROM users WHERE username=? AND password=?;"
	results = cursor.execute(sql,(username,password))
	count = 0
	for row in results:
		count += 1
	if count == 1:
		return True
	else:
		return False

def DBRegister(username,email,password):
	conn = sq.connect('db.sqlite')
	cursor = conn.cursor()
	sql = "INSERT INTO users(username,email,password) VALUES(?,?,?);"
	cursor.execute(sql,(username,email,password))
	conn.commit()
	return True