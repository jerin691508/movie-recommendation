# backend/recommender/ml/hybrid.py
from .collaborative import predict_user_scores
from .content import get_content_similar_movies
import numpy as np

def normalize_scores(scores):
    """Normalize dict of {item: score} to 0..1 range."""
    if not scores:
        return {}
    vals = np.array(list(scores.values()), dtype=float)
    mn, mx = vals.min(), vals.max()
    if mx == mn:
        return {k: 0.0 for k in scores}
    return {k: (v - mn) / (mx - mn) for k, v in scores.items()}

def recommend_for_user(user_id, top_k=20, alpha=0.6, beta=0.4):
    """
    alpha: weight of collaborative score
    beta: weight of content score
    Returns list of movie ids.
    """
    # Collaborative: get a ranked list -> convert to score
    coll_list = predict_user_scores(user_id, top_k=500)
    coll_scores = {mid: (len(coll_list) - i) for i, mid in enumerate(coll_list)} if coll_list else {}
    coll_norm = normalize_scores(coll_scores)

    # Content: expand from top coll_list movies (or top popular) to get neighborhood votes
    content_scores = {}
    for mid in (coll_list[:100] if coll_list else []):
        neighbors = get_content_similar_movies(mid, top_k=10)
        for idx, nmid in enumerate(neighbors):
            content_scores[nmid] = content_scores.get(nmid, 0.0) + (1.0 / (idx + 1.0))

    content_norm = normalize_scores(content_scores)

    # Combine
    combined = {}
    keys = set(coll_norm.keys()) | set(content_norm.keys())
    for k in keys:
        cscore = coll_norm.get(k, 0.0)
        tscore = content_norm.get(k, 0.0)
        combined[k] = alpha * cscore + beta * tscore

    sorted_items = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return [int(item_id) for item_id, _ in sorted_items[:top_k]]
