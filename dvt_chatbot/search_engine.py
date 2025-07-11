import json
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict
from dvt_chatbot.config import DVT_GUIDE_FILE

# Load once at module level
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def clean_content(text: str) -> str:
    # Collapse all whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove common irrelevant phrases or blocks
    patterns = [
        r"Skip to content",
        r"Back to top",
        r"Toggle navigation menu.*?⌘ K.*?",  # keyboard shortcut banner
        r"DVT SystemVerilog IDE for Eclipse User Guide",  # repeated title
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text.strip()

def load_guide_chunks(data_path: str = DVT_GUIDE_FILE) -> List[Dict]:
    with open(data_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    for chunk in chunks:
        if "content" in chunk:
            chunk["content"] = clean_content(chunk["content"])

    return chunks

def find_best_semantic_match(query: str, chunks: List[Dict], threshold: float = 0.5, model=None) -> Dict | None:
    embed_model = model or embedder
    query_embedding = embed_model.encode(query)

    best_score = -1
    best_entry = None

    for entry in chunks:
        embedding = entry.get("embedding")
        if not embedding:
            continue
        score = cosine_similarity(query_embedding, embedding)
#        print(f"[TEST DEBUG] Similarity score: {score}")
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_score >= threshold and best_entry:
        return {
            "title": best_entry["title"],
            "url": best_entry["url"],
            "content": best_entry["content"],
            "score": best_score,
        }

    return None

# Optional: keep search_guide if you want top_k results instead of best one
def search_guide(query: str, data_path: str = DVT_GUIDE_FILE, top_k: int = 3) -> List[Tuple[float, str, str, str]]:
    chunks = load_guide_chunks(data_path)
    query_embedding = embedder.encode(query)
    results = []
    for entry in chunks:
        vec = entry.get("embedding")
        if vec:
            sim = cosine_similarity(query_embedding, vec)
            results.append((sim, entry["title"], entry["url"], entry["content"]))

    # Sort by descending similarity
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_k]
