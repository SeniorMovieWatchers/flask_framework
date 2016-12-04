import MySQLdb
import csv
import imdb
import numpy as np
links_path = '/srv/movielens/links.csv'
movie_path = '/srv/movielens/movies.csv'
rating_path = '/srv/movielens/ratings.csv'
genome_path = '/srv/movielens/genome-tags.csv'
scores_path = '/srv/movielens/genome-scores.csv'
ia = imdb.IMDb()
db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='cs411fa2016', db='movielens')
cur = db.cursor()
import_movie = True
import_ratings = False
import_genome = False
import_scores = False

movie_id_to_index = {}
index_to_imdb = {}
imdb_ids = set()
index = 0
with open(links_path, 'rb') as f:
    next(f)
    for movie_id, imdb_id, _ in csv.reader(f):
        movie_id = int(movie_id)
        imdb_id = int(imdb_id)
        if imdb_id not in imdb_ids:
            movie_id_to_index[movie_id] = index
            index_to_imdb[index] = imdb_id
            imdb_ids.add(imdb_id)
            index += 1
        else:
            for key, value in index_to_imdb.items():
                if value == imdb_id:
                    movie_id_to_index[movie_id] = key

def get(movie, key):
    if movie.has_key(key):
        return movie[key]
    else:
        return 'NULL'
def get_list(movie, key):
    if movie.has_key(key):
        return '||'.join(movie[key])
    else:
        return 'NULL'

skip = 20920
if import_movie:
    imported = set()
    with open(movie_path, 'rb') as f:
        next(f)
        for movie_id, title, genres in csv.reader(f):
            movie_id = int(movie_id)
            if movie_id not in movie_id_to_index:
                continue
            imdb_id = index_to_imdb[movie_id_to_index[movie_id]]
            if imdb_id in imported:
                continue
            if skip > 0:
                skip -= 1
                continue
            movie = ia.get_movie(imdb_id)
            try:
                #ia.update(movie, ['year', 'cover url', 'mpaa', 'plot', 'languages', 'genre'])
                ia.update(movie)
                cur.execute("Insert ignore into movie values(%s,%s,%s,%s,%s,%s,%s,%s)", (imdb_id, title, get(movie, 'year'), get(movie, 'cover url'), get(movie, 'mpaa'), get_list(movie, 'plot'), get_list(movie, 'genre'), get_list(movie, 'languages')))            

                for role in ['writer', 'production manager', 'cast', 'editor', 'visual effects', 'producer', 'cast', 'production designer', 'special effects department']:
                    if not movie.has_key(role):
                        continue
                    for person in movie[role]:
                        person_id = person.getID()
                        name = person['name']
                        cur.execute('insert ignore into person values(%s,%s)', (person_id, name))
                        cur.execute('insert ignore into person_junction values(%s,%s,%s)', (person_id, role, imdb_id))
                
                imported.add(imdb_id)
                db.commit()
            except:
                pass

if import_genome:
    with open(genome_path, 'rb') as f:
        next(f)
        for tag_id, tag in csv.reader(f):
            cur.execute("Insert into genome(id, tag) values(%s, %s)", (tag_id, tag))


if import_ratings:
    count = 0
    rated = set()
    with open(rating_path, 'rb') as f:
        next(f)
        for user_id, movie_id, rating, timestamp in csv.reader(f):
            movie_id = int(movie_id)
            if movie_id in movie_id_to_index:
                imdb_id = index_to_imdb[movie_id_to_index[movie_id]]
                if (user_id, imdb_id) not in rated:
                    rating = int(rating.replace('.', ''))
                    cur.execute("Insert into ratings(user_id,movie_id,rating,timestamp) values(%s,%s,%s,%s)", (user_id, imdb_id, rating, timestamp))
                    rated.add((user_id, imdb_id))
                    count += 1
                    if count % 10000 == 0:
                        print(count)
                        db.commit()


if import_scores:
    scored = set()
    count = 0
    with open(scores_path, 'rb') as f:
        next(f)
        for movie_id, tag_id, relevance in csv.reader(f):
            movie_id = int(movie_id)
            if movie_id in movie_id_to_index:
                imdb_id = index_to_imdb[movie_id_to_index[movie_id]]
                if (imdb_id, tag_id) not in scored:
                    cur.execute("Insert into genome_scores(movie_id, tag_id, relevance) values(%s, %s, %s)", (imdb_id, tag_id, relevance))
                    count += 1
                    scored.add((imdb_id, tag_id))
                    if count % 10000 == 0:
                        print(count)
                        db.commit()

db.commit()
db.close()
