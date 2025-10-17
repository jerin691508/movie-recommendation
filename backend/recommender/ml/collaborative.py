# backend/recommender/ml/collaborative.py
import joblib
import numpy as np
import os
from scipy.sparse import csr_matrix, save_npz, load_npz
from scipy.sparse.linalg import svds

FEATURE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..', 'data', 'features')
os.makedirs(FEATURE_DIR, exist_ok=True)

def build_rating_matrix(ratings_df, save_prefix=FEATURE_DIR):
    """
    ratings_df: pandas DataFrame with columns ['user_id', 'movie_id', 'rating']
    Creates a CSR matrix (users x items) and saves it, plus users/movies index lists.
    """
    users_list = sorted(ratings_df['user_id'].unique().tolist())
    movies_list = sorted(ratings_df['movie_id'].unique().tolist())
    users_map = {u: i for i, u in enumerate(users_list)}
    movies_map = {m: i for i, m in enumerate(movies_list)}

    rows = ratings_df['user_id'].map(users_map).to_numpy()
    cols = ratings_df['movie_id'].map(movies_map).to_numpy()
    data = ratings_df['rating'].astype(float).to_numpy()

    matrix = csr_matrix((data, (rows, cols)), shape=(len(users_list), len(movies_list)))

    save_npz(os.path.join(save_prefix, 'ratings_matrix.npz'), matrix)
    joblib.dump(users_list, os.path.join(save_prefix, 'users_index.joblib'))
    joblib.dump(movies_list, os.path.join(save_prefix, 'movies_index.joblib'))
    return matrix, users_map, movies_map

def train_svd(ratings_matrix, k=50, save_prefix=FEATURE_DIR):
    """
    ratings_matrix: scipy csr_matrix
    Trains truncated SVD and saves u, s, vt and user_means.
    """
    R = ratings_matrix.toarray()
    # user means ignoring zeros
    user_means = np.true_divide(R.sum(1), (R != 0).sum(1), where=(R != 0).sum(1) != 0)
    R_filled = R.copy()
    for i in range(R.shape[0]):
        if (R[i] == 0).all():
            R_filled[i] = 0.0
        else:
            mean = user_means[i] if not np.isnan(user_means[i]) else 0.0
            R_filled[i, R[i] == 0] = mean

    u, s, vt = svds(R_filled, k=k)
    # reorder descending
    idx = np.argsort(-s)
    u, s, vt = u[:, idx], s[idx], vt[idx, :]

    np.save(os.path.join(save_prefix, 'svd_u.npy'), u)
    np.save(os.path.join(save_prefix, 'svd_s.npy'), s)
    np.save(os.path.join(save_prefix, 'svd_vt.npy'), vt)
    joblib.dump(user_means.tolist(), os.path.join(save_prefix, 'user_means.joblib'))
    return u, s, vt

def load_collab_artifacts():
    try:
        users_list = joblib.load(os.path.join(FEATURE_DIR, 'users_index.joblib'))
        movies_list = joblib.load(os.path.join(FEATURE_DIR, 'movies_index.joblib'))
        u = np.load(os.path.join(FEATURE_DIR, 'svd_u.npy'))
        s = np.load(os.path.join(FEATURE_DIR, 'svd_s.npy'))
        vt = np.load(os.path.join(FEATURE_DIR, 'svd_vt.npy'))
        user_means = joblib.load(os.path.join(FEATURE_DIR, 'user_means.joblib'))
        return users_list, movies_list, u, s, vt, user_means
    except Exception:
        return None, None, None, None, None, None

def predict_user_scores(user_id, top_k=20):
    """
    Return top_k movie IDs predicted for user_id using reconstructed SVD approximation.
    If user is not known, return empty list (cold start handled elsewhere).
    """
    users_list, movies_list, u, s, vt, user_means = load_collab_artifacts()
    if users_list is None:
        return []

    if user_id not in users_list:
        return []

    approx = u.dot(np.diag(s)).dot(vt)  # users x items
    uid = users_list.index(user_id)
    scores = approx[uid]
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [int(movies_list[i]) for i in top_indices]
