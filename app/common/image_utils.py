import requests
import base64
from app.config import GEMINI_API_KEY

from pathlib import Path
from app.config import BASE_DIR

IMAGE_DIR = BASE_DIR / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True, parents=True)

def generate_meme_image(...):
    ...
    path = IMAGE_DIR / f"{job_prefix}.png"
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path


def generate_meme_image(prompt, job_prefix):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateImage"
    params = {"key": GEMINI_API_KEY}

    payload = {
        "prompt": prompt,
        "size": "1024x1024"
    }

    resp = requests.post(url, json=payload, params=params)
    resp.raise_for_status()
    data = resp.json()

    b64 = data["candidates"][0]["image"]["base64"]
    img = base64.b64decode(b64)

    path = IMAGE_DIR / f"{job_prefix}.png"
    with open(path, "wb") as f:
        f.write(img)

    return path
