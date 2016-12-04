import mysql.connector as mariadb

database = mariadb.connect(user='root',
#	password='cs411fa2016',
	password='301114',
	database='movielens')

cursor = database.cursor(buffered=True)
