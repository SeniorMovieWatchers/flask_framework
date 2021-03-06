from flask import Flask, render_template, request, jsonify
from db import database, cursor

NUM_RECOMMENDATIONS = 5

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
        sql_query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(sql_query, tuple([email]))
        if cursor.rowcount == 0:
            sql_query = "INSERT INTO user(id, username, email) VALUES(%s, %s, %s)"
            cursor.execute(sql_query, tuple([id, username, email]))
            database.commit()
            return "SUCCESS"
    return "FAILED"

@app.route("/search-movie", methods=["POST"])
def search_movie():
    if request.method == "POST":
        keyword = request.json["keyword"]
        sql_query = "SELECT * FROM movie WHERE title LIKE %s"
        cursor.execute(sql_query, tuple(['%' + keyword + '%']))
        rows = cursor.fetchmany(size=5)
        movie_list = []
        for row in rows:
            movie = get_movie_details(row)
            movie_list.append(movie)
        result = {"movie_list": movie_list}
        return jsonify(result)


@app.route("/get-favorite", methods=["POST"])
def get_favorite():
    if request.method == "POST":
        user_id = request.json["user_id"]
        sql_query = "SELECT movie_id FROM user_favorite WHERE user_id = %s"
        cursor.execute(sql_query, tuple([user_id]))
        rows = cursor.fetchall()
        movie_list = []
        for movie_id in rows:
            movie_id = movie_id[0]
            sql_query = "SELECT * FROM movie WHERE id = %s"
            cursor.execute(sql_query, tuple([movie_id]))
            movie_row = cursor.fetchone()
            movie = get_movie_details(movie_row)
            movie_list.append(movie)
        result = {"favorite_movies": movie_list}
        return jsonify(result)


@app.route("/add-favorite", methods=["POST"])
def add_favorite():
    if request.method == "POST":
        user_id = request.json["user_id"]
        movie_id = request.json["movie_id"]
        sql_query = "INSERT INTO user_favorite(user_id, movie_id) VALUES(%s, %s)"
        cursor.execute(sql_query, tuple([user_id, movie_id]))
        database.commit()
        return "SUCCESS"
    return "FAILED"


import ratings_matrix
from similarity import get_matches
@app.route("/get-recommendation", methods=["POST"])
def get_recommendation():
    if request.method == "POST":
        RATINGS_PATH = '/srv/movielens/ratings_matrix.npz'
        RATINGS_MATRIX = ratings_matrix.ratings_matrix(RATINGS_PATH)
        user_id = request.json["user_id"]
        sql_query = "SELECT DISTINCT movie_id FROM user_favorite WHERE user_id = %s"
        cursor.execute(sql_query, tuple([user_id]))
        movie_ids = cursor.fetchall()
        movie_list = []
        if len(movie_ids) == 0:
            result = {"recommended_movies": movie_list}
            return jsonify(result)

        liked = {}
        for movie_id in movie_ids:
	    movie_id = movie_id[0]
            liked[movie_id] = 50
	print (liked)
        recommendations = get_matches(RATINGS_MATRIX, liked, NUM_RECOMMENDATIONS)
	print (recommendations)
        sql_query = "SELECT * FROM movie WHERE id = %s"
        for index in range(NUM_RECOMMENDATIONS):
            movie_id = recommendations[index][1]
            movie_id = RATINGS_MATRIX.imdb_id(movie_id)
            cursor.execute(sql_query, tuple([int(movie_id)]))
            movie_row = cursor.fetchone()
            movie = get_movie_details(movie_row)
            movie_list.append(movie)
        result = {"recommended_movies": movie_list}
	print (movie_list)
        return jsonify(result) 


def get_movie_details(row):
    id = row[0]
    sql_query = "SELECT person.name FROM person, person_junction " +\
                "WHERE person.id = person_junction.person_id" +\
                " AND person_junction.role = 'cast'" +\
                " AND person_junction.movie_id = %s"
    cursor.execute(sql_query, tuple([id]))
    casts = cursor.fetchmany(size=4)
    actors = []
    for cast in casts:
        actors.append(cast[0])
    sql_query = "SELECT rating FROM ratings WHERE movie_id = %s"
    cursor.execute(sql_query, tuple([id]))
    rating = cursor.fetchone()[0]
    movie = {
        "id" : row[0],
        "title": row[1],
        "year": row[2],
        "url": row[3],
        "plot": row[5][:200] + " ...",
        "genre": row[6],
        "language": row[7],
        "casts": actors,
        "rating": rating
    }
    return movie


if __name__ == "__main__":
  app.run(host="0.0.0.0")
