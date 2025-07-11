# dvt_chatbot/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env variables if present (optional)
load_dotenv()

DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"

# Calculate project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Default paths, overridable via env
CUSTOM_ANSWERS_FILE = os.getenv("CUSTOM_ANSWERS_FILE", str(DATA_DIR / "custom_answers.yaml"))
DVT_GUIDE_FILE = os.getenv("DVT_GUIDE_FILE", str(DATA_DIR / "dvt_guide_data_with_embeddings.json"))

print(f"[DEBUG] BASE_DIR: {BASE_DIR}")
print(f"[DEBUG] DATA_DIR: {DATA_DIR}")
print(f"[DEBUG] CUSTOM_ANSWERS_FILE: {CUSTOM_ANSWERS_FILE}")