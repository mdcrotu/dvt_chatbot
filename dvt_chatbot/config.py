from dotenv import load_dotenv
import os

load_dotenv()

CUSTOM_ANSWERS_FILE = os.getenv("CUSTOM_ANSWERS_FILE", "custom_answers.yaml")
DVT_GUIDE_FILE = os.getenv("DVT_GUIDE_FILE", "dvt_guide_data_with_embeddings.json")
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
