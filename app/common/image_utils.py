# app/common/image_utils.py

import base64
import requests
from pathlib import Path

from app.config import (
    BASE_DIR,
    ENABLE_IMAGE_GENERATION,
)
import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 이미지 저장 폴더
IMAGE_DIR = BASE_DIR / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True, parents=True)


def generate_meme_image(meme_prompt: str, job_prefix: str):
    """
    Google Gemini (Imagen) API를 이용해 이미지 생성
    - 이미지 생성 비활성화면 None 반환
    - 실패해도 None 반환 (프로세스 계속 진행)
    - 성공하면 Path 객체 반환
    """

    if not ENABLE_IMAGE_GENERATION:
        print("[IMAGE] Skipped - ENABLE_IMAGE_GENERATION = False")
        return None

    if not GEMINI_API_KEY:
        print("[IMAGE] Skipped - GEMINI_API_KEY not set")
        return None

    print("[IMAGE] Generating image via Google Gemini...")

    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "imagegeneration:generateImage"
        )

        params = {
            "key": GEMINI_API_KEY
        }

        payload = {
            "prompt": {
                "text": meme_prompt
            },
            "aspectRatio": "1:1"
        }

        resp = requests.post(
            url,
            json=payload,
            params=params,
            timeout=120
        )

        if resp.status_code != 200:
            print("[IMAGE] Gemini request failed:", resp.status_code, resp.text)
            return None

        data = resp.json()

        # Google 이미지 API 기준 구조
        images = data.get("images")
        if not images:
            print("[IMAGE] No image returned from Gemini:", data)
            return None

        b64 = images[0].get("imageBytes")
        if not b64:
            print("[IMAGE] imageBytes missing")
            return None

        img_bytes = base64.b64decode(b64)

        path = IMAGE_DIR / f"{job_prefix}.png"
        with open(path, "wb") as f:
            f.write(img_bytes)

        print(f"[IMAGE] Saved image → {path}")
        return path

    except Exception as e:
        print(f"[IMAGE] ERROR: {e}")
        return None
