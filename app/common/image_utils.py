import base64
from pathlib import Path
from openai import OpenAI
from app.config import OPENAI_API_KEY, BASE_DIR

client = OpenAI(api_key=OPENAI_API_KEY)

IMAGE_DIR = BASE_DIR / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True)


def generate_meme_image(meme_prompt: str, job_prefix: str):
    print("[IMAGE] Skipped - image generation temporarily disabled")
    return None