import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

WP_CATEGORY_US_TECH = int(os.getenv("WP_CAT_US_TECH", "0"))
WP_CATEGORY_KR_TECH = int(os.getenv("WP_CAT_KR_TECH", "0"))
WP_CATEGORY_GAME = int(os.getenv("WP_CAT_GAME", "0"))

DATA_PATH = BASE_DIR / "data.json"

ENABLE_IMAGE_GENERATION = os.getenv("ENABLE_IMAGE_GENERATION", "false").lower() == "true"
