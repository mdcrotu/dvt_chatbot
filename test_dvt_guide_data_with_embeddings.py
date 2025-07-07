import json

with open("dvt_guide_data_with_embeddings.json") as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")
print("Keys in first entry:", data[0].keys())
print("Embedding length:", len(data[0]['embedding']))
print("First 5 values:", data[0]['embedding'][:5])
