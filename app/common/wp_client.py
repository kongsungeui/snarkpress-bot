import re
import requests
from requests.auth import HTTPBasicAuth
from app.config import WP_URL, WP_USER, WP_APP_PASSWORD

auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)


def upload_media(image_path, alt_text=""):
    """
    이미지 업로드 -> media_id 반환
    JPEG/PNG 둘 다 지원
    """
    url = f"{WP_URL}/wp-json/wp/v2/media"
    filename = image_path.name

    suffix = image_path.suffix.lower()
    if suffix in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        mime = "image/png"

    with open(image_path, "rb") as f:
        files = {"file": (filename, f, mime)}
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

    body_markdown = _ensure_links_open_in_new_tab(body_markdown)

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


def _ensure_links_open_in_new_tab(html: str) -> str:
    """
    Adds target="_blank" and rel attributes to anchor tags that lack them so that
    source links open in a new tab.
    """

    def _replace(match: re.Match) -> str:
        anchor_tag = match.group(0)
        if "target=" in anchor_tag:
            return anchor_tag
        # Insert attributes right after the opening <a
        return anchor_tag.replace("<a", '<a target="_blank" rel="noopener noreferrer"', 1)

    return re.sub(r"<a[^>]*>", _replace, html)
