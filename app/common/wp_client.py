import requests
from requests.auth import HTTPBasicAuth
from app.config import WP_URL, WP_USER, WP_APP_PASSWORD

auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)


def upload_media(image_path, alt_text=""):
    """
    이미지 업로드 -> media_id 반환
    """
    url = f"{WP_URL}/wp-json/wp/v2/media"
    filename = image_path.name

    with open(image_path, "rb") as f:
        files = {
            "file": (filename, f, "image/png")
        }
        data = {"alt_text": alt_text}
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }

        r = requests.post(url, auth=auth, files=files, data=data, headers=headers)

    r.raise_for_status()
    return r.json()["id"]


def create_post(title, body_markdown, cynical_comment, meme_media_id, category_id):
    """
    워드프레스 글 발행
    """

    url = f"{WP_URL}/wp-json/wp/v2/posts"

    content = f"""
{body_markdown}

<hr/>

> {cynical_comment}
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
