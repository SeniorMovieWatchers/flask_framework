from flask import Flask, render_template, request, jsonify
from db import database, cursor

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/signin", methods=["POST"])
def sign_in():
    if request.method == "POST":
        id = request.json["id"]
        username = request.json["username"]
        email = request.json["email"]
        sql_query = "SELECT * FROM user WHERE email='%s'" % email
        cursor.execute(sql_query)
        if cursor.rowcount == 0:
            sql_query = "INSERT INTO user(id, username, email) values('%s', '%s', '%s')" % (id, username, email)
            cursor.execute(sql_query)
            database.commit()
    return "Unsuccessful POST request"


@app.route("/search-movie", methods=["POST"])
def search_movie():
    if request.method == "POST":
        keyword = request.json["keyword"]
        sql_query = "SELECT * FROM movie WHERE title LIKE '%" + keyword +"%'"
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        print (rows)
    return "Unsuccessful POST request"


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

if __name__ == "__main__":
  app.run(host="0.0.0.0")
