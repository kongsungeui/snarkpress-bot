# app/common/image_utils.py

import base64
import os
from pathlib import Path

import requests

from app.config import BASE_DIR, ENABLE_IMAGE_GENERATION

# Gemini API 키 (.env 에 GEMINI_API_KEY 있어야 함)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 이미지 저장 폴더
IMAGE_DIR = BASE_DIR / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True, parents=True)


def generate_meme_image(meme_prompt: str, job_prefix: str):
    """
    Google Gemini 2.5 Flash Image REST API로 밈 이미지 생성.

    - ENABLE_IMAGE_GENERATION=false 이거나 GEMINI_API_KEY 없으면 None 반환
    - API 요청 실패해도 None 반환 (글 발행은 계속 진행)
    - 성공하면 생성된 PNG 파일의 Path 반환
    """

    if not ENABLE_IMAGE_GENERATION:
        print("[IMAGE] Skipped - ENABLE_IMAGE_GENERATION = False")
        return None

    if not GEMINI_API_KEY:
        print("[IMAGE] Skipped - GEMINI_API_KEY not set")
        return None

    print("[IMAGE] Generating image via Gemini 2.5 Flash Image...")

    # 공식 문서 기준 REST 엔드포인트
    # POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent
    # headers: x-goog-api-key, Content-Type: application/json
    # body: { "contents": [{ "parts": [ {"text": "..."} ] }], "generationConfig": { "responseModalities": ["Image"], "imageConfig": { "aspectRatio": "1:1" } } }
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash-image:generateContent"
    )

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": meme_prompt}
                ]
            }
        ],
        "generationConfig": {
            # 텍스트는 필요 없고 이미지만 받도록 설정
            "responseModalities": ["Image"],
            "imageConfig": {
                "aspectRatio": "1:1",
            },
        },
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
    except Exception as e:
        print(f"[IMAGE] Request error: {e}")
        return None

    if resp.status_code != 200:
        print("[IMAGE] Gemini request failed:", resp.status_code, resp.text)
        return None

    data = resp.json()

    # 응답 구조: candidates[0].content.parts[*].inlineData.data (base64)
    try:
        candidates = data.get("candidates") or []
        if not candidates:
            print("[IMAGE] No candidates in Gemini response")
            return None

        parts = candidates[0]["content"]["parts"]
        b64_data = None
        for part in parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                b64_data = inline["data"]
                break

        if not b64_data:
            print("[IMAGE] No inlineData.data (image) found in response")
            return None

        img_bytes = base64.b64decode(b64_data)

        path = IMAGE_DIR / f"{job_prefix}.png"
        with open(path, "wb") as f:
            f.write(img_bytes)

        print(f"[IMAGE] Saved image → {path}")
        return path

    except Exception as e:
        print(f"[IMAGE] Parse error: {e} | raw response: {data}")
        return None
