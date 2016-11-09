import MySQLdb
import similarity as sim
import numpy as np
import ratings_matrix
from similarity import get_matches

ratings_path = '/srv/movielens/ratings_matrix.npz'
num_movies = 50

print_favorites = True
print_recommendations = True
print_plots = False

db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='cs411fa2016', db='movielens')
cur = db.cursor()

'''
ratings = csr_matrix(np.array([[1, 2, 0, 0, 1], [3, 2, 1, 1, 0], [5, 2, 1, 0, 0], [20, 20, 3, 3, 3]]))
watched = {0:5, 1:2}
'''
ratings_matrix = ratings_matrix.ratings_matrix(ratings_path)
#movie_ids, ratings = load_sparse(ratings_path)
person = 34
#person = 35
watched = {}
ids = []
for movie_id, rating in ratings_matrix.each_movie(person):
    watched[movie_id] = rating
    ids.append(ratings_matrix.imdb_id(movie_id))

if print_favorites:
    format_strings = ','.join(['%s'] * len(ids))
    cur.execute("select title from movie where id in (%s)" % format_strings, tuple(ids))
    for title in cur.fetchall():
        print(title)

print('recommended')

recommendations = get_matches(ratings_matrix, watched, num_movies)
for index in range(20):
    try:
        rating, movie_id = recommendations[index]
        movie_id = ratings_matrix.imdb_id(movie_id)

        if print_recommendations:
            cur.execute('select title from movie where id=%s', movie_id)
            print(cur.fetchone()[0], rating)
    except:
        pass

db.close()
