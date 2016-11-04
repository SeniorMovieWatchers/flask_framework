from flask import Flask, render_template, request, jsonify
from db import database, cursor

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
  return render_template('index.html')

@app.route("/new-user", methods=["POST"])
def new_user():
  if request.method == "POST":
    username = request.json['username']
    email    = request.json['email']
    password = request.json['password']
    sql_query = "INSERT INTO user(username, email, password) values('%s', '%s', '%s')"%(username, email, password)
    cursor.execute(sql_query)
    database.commit()
    return sql_query
  return "Unsuccessful POST request"

@app.route("/update-username", methods=["POST"])
def update_email():
  if request.method == "POST":
    username = request.json['username']
    email   = request.json['email']
    sql_query = "UPDATE user SET username='%s' WHERE email='%s'"%(username, email)
    cursor.execute(sql_query)
    database.commit()
    return sql_query
  return "Unsuccessful POST request"

@app.route("/search-user-email", methods=["POST"])
def search_user_email():
  if request.method == "POST":
     email = request.json['email']
     sql_query = "SELECT * FROM user WHERE email='%s'"%email
     cursor.execute(sql_query)
     user_list = []
     for id, username, email, password in cursor:    
       user = {"username" : username,
               "email"    : email,
               "id" : id}
       user_list.append(user)
     result = {"query":sql_query, "user_list":user_list}
     return jsonify(result)

@app.route("/search-user-username", methods=["POST"])
def search_user_username():
  if request.method == "POST":
     username = request.json['username']
     sql_query = "SELECT * FROM user WHERE username='%s'"%username
     cursor.execute(sql_query)
     user_list = []
     for id, username, email, password in cursor:
       user = {"username" : username,
               "email"    : email,
               "id" : id}
       user_list.append(user)
     result = {"query":sql_query, "user_list":user_list}
     return jsonify(result) 

@app.route("/duplicate-email", methods=["GET"])
def duplicate_email():
  if request.method == "GET":
     sql_query = "SELECT u1.username, u1.email, u1.id FROM user u1, user u2 WHERE u1.email = u2.email AND u1.id <> u2.id"
     cursor.execute(sql_query)
     user_list = []
     for username, email, id in cursor:
       user = {"username" : username,
               "email"    : email,
               "id" : id}
       user_list.append(user)
     result = {"query":sql_query, "user_list":user_list}
     return jsonify(result)

if __name__ == "__main__":
  import logging, sys
  logging.basicConfig(stream=sys.stderr)  

  app.run(host="0.0.0.0")
