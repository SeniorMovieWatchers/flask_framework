import mysql.connector as mariadb

database = mariadb.connect(user='root',
	password='cs411fa2016',
	database='imdb')

cursor = database.cursor()
