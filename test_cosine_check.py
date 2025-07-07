import json
from numpy import dot
from numpy.linalg import norm

# Step 1: Load the embedded JSON
with open("dvt_guide_data_with_embeddings.json", "r") as f:
    data = json.load(f)

# Step 2: Pick two different sections
a = data[0]['embedding']
b = data[1]['embedding']
print(data[0]['title'])
print(data[1]['title'])

# Step 3: Compute cosine similarity
similarity = dot(a, b) / (norm(a) * norm(b))
print(f"Cosine similarity between section 0 and 1: {similarity:.3f}")
