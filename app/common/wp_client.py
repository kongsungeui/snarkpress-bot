import requests
from requests.auth import HTTPBasicAuth
from app.config import WP_URL, WP_USER, WP_APP_PASSWORD

auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)


def upload_media(image_path, alt_text=""):
    url = f"{WP_URL}/wp-json/wp/v2/media"
    filename = image_path.name

    with open(image_path, "rb") as f:
        files = {"file": (filename, f, "image/png")}
        data = {"alt_text": alt_text}
        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
        r = requests.post(url, auth=auth, files=files, data=data, headers=headers)

    r.raise_for_status()
    return r.json()["id"]


def create_post(title, body_markdown, cynical_comment, meme_media_id, category_id):
    """
    워드프레스 글 발행
    - 상단에 "오늘의 한줄 냉소" 블록을 굵게/박스로 강조
    """

    url = f"{WP_URL}/wp-json/wp/v2/posts"

    content = f"""
<div style="border: 2px solid #eee; padding: 12px 14px; border-radius: 8px; background-color: #fafafa; margin-bottom: 18px;">
  <strong>💬 오늘의 한줄 냉소</strong><br/>
  <span style="font-style: italic;">{cynical_comment}</span>
</div>

{body_markdown}
"""

    data = {
        "title": title,
        "content": content,
        "status": "publish",
    }

    if meme_media_id:
        data["featured_media"] = meme_media_id

    if category_id:
        data["categories"] = [category_id]

    r = requests.post(url, auth=auth, json=data)
    r.raise_for_status()
    return r.json()
