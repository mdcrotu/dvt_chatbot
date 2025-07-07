import json
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(vec1, vec2):
    if not vec1 or not vec2:
        return 0.0
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def validate_embeddings(file_path="dvt_guide_data_with_embeddings.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load file: {e}")
        return

    if not data or 'embedding' not in data[0]:
        print("❌ No embeddings found in the data.")
        return

    print(f"✅ Loaded {len(data)} entries with embeddings.")
    print(f"🔍 Checking first 5 embeddings...")

    for i in range(min(5, len(data))):
        emb = data[i]['embedding']
        print(f" - Entry {i} | Length: {len(emb)} | Title: {data[i]['title']}")

    if len(data) > 1:
        print("\n📏 Cosine similarity between first two entries:")
        sim = cosine_similarity(data[0]['embedding'], data[1]['embedding'])
        print(f'   "{data[0]["title"]}" ⟷ "{data[1]["title"]}" → Similarity: {sim:.3f}')

if __name__ == "__main__":
    validate_embeddings()
