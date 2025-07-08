import json
import os
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Load guide data
INPUT_FILE = 'dvt_guide_data.json'
OUTPUT_FILE = 'dvt_guide_data_with_embeddings.json'

def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    print("Loading guide data...")
    guide_data = load_data(INPUT_FILE)

    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Embedding content...")
    for entry in tqdm(guide_data):
        content = entry.get('content', '')
        embedding = model.encode(content).tolist()
        entry['embedding'] = embedding

    print(f"Saving embedded data to {OUTPUT_FILE}...")
    save_data(guide_data, OUTPUT_FILE)
    print("Done.")

if __name__ == "__main__":
    main()
