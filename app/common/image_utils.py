import base64
from pathlib import Path
from openai import OpenAI
from app.config import OPENAI_API_KEY, BASE_DIR

client = OpenAI(api_key=OPENAI_API_KEY)

IMAGE_DIR = BASE_DIR / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True)


def generate_meme_image(meme_prompt: str, job_prefix: str) -> Path:
    """
    meme_prompt -> 이미지 생성
    return Path("파일 경로")
    """

    resp = client.images.generate(
        model="gpt-image-1",
        prompt=meme_prompt,
        size="1024x1024",
        n=1,
    )

    b64 = resp.data[0].b64_json
    img_bytes = base64.b64decode(b64)

    path = IMAGE_DIR / f"{job_prefix}.png"

    with open(path, "wb") as f:
        f.write(img_bytes)

    return path
