import numpy as np

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
    return choices
#return [movie for score, movie in choices]
