import numpy as np
import numpy.random as rand
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

def intersect(ratings, other_id, watched):
    person_ratings = []
    other_ratings = []
    for movie_id, rating in ratings.each_movie(other_id):
        if movie_id in watched:
            person_ratings.append(watched[movie_id])
            other_ratings.append(rating)
    return person_ratings, other_ratings

def update_centroids(ratings, indices):
    centroids = np.zeros((100, ratings.movie_count()))
    count = [defaultdict(int) for _ in range(100)]
    for person_id in ratings.each_user():
        centroid = indices[person_id]
        for movie_id, movie_rating in ratings.each_movie(person_id):
            centroids[centroid, movie_id] += movie_rating
            count[centroid][movie_id] += 1
    for centroid in range(len(count)):
        for movie_id, ct in count[centroid].items():
            centroids[centroid, movie_id] /= ct
    return centroids

def indices(ratings, centroids):
    index = []
    for person_id in ratings.each_user():
        best_centroid = 0
        best_dist = float('inf')
        for centroid_index in range(len(centroids)):
            centroid_ratings, person_ratings = intersect(ratings, person_id, centroids[centroid_index])
            if centroid_ratings:
                dist = cosine_similarity ([centroid_ratings], [person_ratings])
                if dist < best_dist:
                    best_dist = dist
                    best_centroid = centroid_index
        index.append(best_centroid)
    return index

def cluster(ratings):
    users = ratings.user_count()
    centroids = rand.rand(100, ratings.movie_count()) * 50

    iterations = 10
    for iteration in range(iterations):
        print(iteration)
        index = indices(ratings, centroids)
        centroids = update_centroids(ratings, index)

    return centroids

def calculate_similarities(ratings, watched):
    sims = np.zeros(ratings.user_count())
    for other_id in ratings.each_user():
        person_ratings, other_ratings = intersect(ratings, other_id, watched)
        if person_ratings:
            sims[other_id] = cosine_similarity ([person_ratings], [other_ratings])
            if len(person_ratings) < 10:
                sims[other_id] /= 11 - len(person_ratings)
    return sims

def get_matches(ratings, watched, num_movies, sims = None):
    watched_indices = {}
    for imdb_id in watched.keys():
        matrix_index = ratings.index_from_imdb(imdb_id)
        if matrix_index >= 0:
            watched_indices[matrix_index] = watched[imdb_id]
    watched = watched_indices
    if not sims:
        sims = calculate_similarities(ratings, watched)

    movies = set()
    sim_sum = defaultdict(int)
    total = defaultdict(int)
    
    neighbors = min(len(sims), 10)

    for other_id in sims.argpartition(-neighbors)[-neighbors:]:
        row_similarity = sims[other_id]
        for movie_id, rating in ratings.each_movie(other_id):
            if movie_id not in watched and movie_id not in movies and row_similarity and len(movies) < num_movies:
                movies.add(movie_id)
            if movie_id in movies:
                sim_sum[movie_id] += row_similarity
                total[movie_id] += rating / ratings.total_rating(other_id)
    choices = sorted([(total[movie] / sim_sum[movie], movie) for movie in movies], reverse = True)
    return [ratings.imdb_id(index) for _, index in choices]

