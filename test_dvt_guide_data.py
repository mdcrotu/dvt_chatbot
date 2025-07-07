import json
with open("dvt_guide_data.json") as f:
    data = json.load(f)
print(data[0].keys())  # should include 'title', 'url', 'content', etc.
