# backend/recommender/ml/content.py
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy import sparse
import os

FEATURE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..', 'data', 'features')
os.makedirs(FEATURE_DIR, exist_ok=True)

def build_content_matrix(movies_df, text_field=None, ngram_range=(1,2), max_features=50000):
    """
    movies_df: DataFrame with columns ['id', 'title', 'description', 'genre', ...]
    Produces TF-IDF matrix saved to disk and vectorizer.
    """
    df = movies_df.copy()
    if text_field is None:
        df['metadata_text'] = (df['title'].fillna('') + ' ' +
                               df['description'].fillna('') + ' ' +
                               df['genre'].fillna(''))
    else:
        df['metadata_text'] = df[text_field].fillna('')

    tfv = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features, stop_words='english')
    tfidf_matrix = tfv.fit_transform(df['metadata_text'])

    # save artifacts
    joblib.dump(tfv, os.path.join(FEATURE_DIR, 'content_tfidf_vectorizer.joblib'))
    joblib.dump(df[['id']].reset_index(drop=True), os.path.join(FEATURE_DIR, 'content_movies_index.joblib'))
    sparse.save_npz(os.path.join(FEATURE_DIR, 'content_tfidf_matrix.npz'), tfidf_matrix)
    return tfidf_matrix, tfv

def load_content_artifacts():
    """Return (tfidf_matrix, vectorizer, movies_index_df) or (None, None, None) if missing."""
    try:
        tfidf_matrix = sparse.load_npz(os.path.join(FEATURE_DIR, 'content_tfidf_matrix.npz'))
        tfv = joblib.load(os.path.join(FEATURE_DIR, 'content_tfidf_vectorizer.joblib'))
        movies_index = joblib.load(os.path.join(FEATURE_DIR, 'content_movies_index.joblib'))
        return tfidf_matrix, tfv, movies_index
    except Exception:
        return None, None, None

def get_content_similar_movies(movie_id, top_k=20):
    """
    For a given movie_id, return list of similar movie ids (by TF-IDF cosine similarity).
    """
    tfidf_matrix, tfv, movies_index = load_content_artifacts()
    if tfidf_matrix is None:
        return []

    # movies_index DataFrame has a column 'id'
    id_to_idx = {int(v): int(i) for i, v in movies_index['id'].items()}
    idx = id_to_idx.get(int(movie_id))
    if idx is None:
        return []

    cosine_similarities = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    related_idx = cosine_similarities.argsort()[::-1][1: top_k + 1]  # skip itself
    related_ids = movies_index.iloc[related_idx]['id'].values.tolist()
    return [int(i) for i in related_ids]
