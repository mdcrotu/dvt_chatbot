import json
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from dvt_chatbot.config import DVT_GUIDE_FILE

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search_guide(query: str, data_path: str = DVT_GUIDE_FILE, top_k: int = 3) -> List[Tuple[float, str, str, str]]:
    # Load data
    with open(data_path, 'r', encoding='utf-8') as f:
        guide_data = json.load(f)

    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query)

    # Score all entries
    results = []
    for entry in guide_data:
        doc_vec = entry.get("embedding")
        if doc_vec is None:
            continue
        score = cosine_similarity(query_embedding, doc_vec)
        results.append((score, entry["title"], entry["url"], entry["content"]))

    # Sort by descending similarity
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_k]
