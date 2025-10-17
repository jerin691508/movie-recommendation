# backend/recommender/ml/train.py
"""
Training orchestration: pull data from Django ORM and build artifacts.
Run with Django context, see management command.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import pandas as pd
from recommender.models import Movie, Rating
from .content import build_content_matrix
from .collaborative import build_rating_matrix, train_svd

FEATURE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'features')

def run_training(k_svd=50):
    # 1) Movies -> content matrix
    movies_qs = Movie.objects.all().values('id', 'title', 'description', 'genre')
    movies_df = pd.DataFrame(list(movies_qs))
    if not movies_df.empty:
        print("Building content TF-IDF matrix for", len(movies_df), "movies...")
        build_content_matrix(movies_df)
    else:
        print("No movies found; skipping content build")

    # 2) Ratings -> collaborative matrix and SVD
    ratings_qs = Rating.objects.all().values('user_id', 'movie_id', 'rating')
    ratings_df = pd.DataFrame(list(ratings_qs))
    if not ratings_df.empty:
        print("Building rating matrix for", len(ratings_df), "ratings...")
        mat, users_map, movies_map = build_rating_matrix(ratings_df)
        print("Training SVD...")
        train_svd(mat, k=k_svd)
    else:
        print("No ratings found; skipping collaborative training")

if __name__ == '__main__':
    run_training()
