from db import database, cursor
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import dok_matrix

class ratings_matrix:
    def __init__(self, path=None):
        if path:
            self.load_from_path(path)
        else:
            self.db = database
            self.cur = cursor
            self.load_from_db()

    def load_from_db(self):
        user_count = self.count_unique('ratings', 'user_id')
        movie_count = self.count_unique('ratings', 'movie_id')
        #Use fewer users for now
        user_count = 5000

        index = 0
        self.imdb_ids = np.empty(movie_count)
        imdb_to_index = {}
        self.total_ratings = np.empty(user_count)
        self.ratings = dok_matrix((user_count, movie_count), dtype=np.float64)

        self.cur.execute('select user_id, movie_id, rating from ratings where user_id<=5000')
        for user_id, movie_id, rating in self.cur.fetchall():
            user_id = int(user_id) - 1
            movie_id = int(movie_id)
            rating = float(rating)

            if movie_id in imdb_to_index:
                movie_index = imdb_to_index[movie_id]
            else:
                movie_index = index
                imdb_to_index[movie_id] = movie_index
                self.imdb_ids[index] = movie_id
                index += 1
            self.ratings[user_id, movie_index] = rating
        self.ratings = self.ratings.tocsr()
        for i in range(user_count):
            self.total_ratings[i] = np.sum(self.ratings[i])

    def imdb_id(self, column):
        return self.imdb_ids[column]

    def count_unique(self, table, column):
        self.cur.execute('select count(distinct({})) from {};'.format(column, table))
        return int(self.cur.fetchone()[0])
    def save_to_path(self, path):
        data = self.ratings.data
        indices = self.ratings.indices
        indptr = self.ratings.indptr
        shape = self.ratings.shape
        np.savez(path, imdb_ids=self.imdb_ids, total_ratings=self.total_ratings, data=data, indices=indices, indptr=indptr, shape=shape)

    def load_from_path(self, path):
        loader = np.load(path)
        self.imdb_ids = loader['imdb_ids']
        self.total_ratings = loader['total_ratings']
        self.ratings = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape = loader['shape'])

    def total_rating(self, user_id):
        return self.total_ratings[user_id]

    def each_user(self):
        for row in range(self.user_count()):
            yield row

    def each_movie(self, user_id):
        for i in range(self.ratings.indptr[user_id], self.ratings.indptr[user_id + 1]):
            yield self.ratings.indices[i], self.ratings.data[i]

    def user_count(self):
        return self.ratings.shape[0]
