# app/jobs/job_kr_tech.py
from datetime import date

from app.sources import news_kr
from app.common import gpt_utils, image_utils, wp_client, storage
from app.config import WP_CATEGORY_KR_TECH


NAMESPACE = "kr_tech"


def run():
    today_str = date.today().isoformat()
    print(f"[KR_TECH] Job start for {today_str}")

    # 1. 후보 뉴스 수집
    candidates = news_kr.fetch_candidates(limit_per_feed=5)
    print(f"[KR_TECH] Fetched {len(candidates)} candidates (before filtering)")

    # 2. 오늘 이미 올린 URL은 제외
    filtered = []
    for c in candidates:
        key = f"{c['url']}|{today_str}"
        if storage.is_posted(NAMESPACE, key):
            print(f"[KR_TECH] Skip already posted: {c['url']}")
            continue
        filtered.append(c)

    if not filtered:
        print("[KR_TECH] No new candidates after filtering. Exit.")
        return

    print(f"[KR_TECH] {len(filtered)} candidates after filtering")

    # 3. GPT로 오늘의 뉴스 하나 선택
    picked = gpt_utils.pick_top_item(
        filtered,
        context="한국 IT/테크 업계(대기업, 스타트업, 규제, 정책 등) 기준으로 오늘 가장 임팩트 있는 뉴스를 하나 골라라.",
    )
    print(f"[KR_TECH] Picked: {picked['title']}")

    # 4. GPT로 포스팅 데이터 생성
    post_data = gpt_utils.build_post(picked, tone="kr_tech")
    print("[KR_TECH] Post data generated from GPT")

    # 5. 밈 이미지 생성
    media_id = None
    image_path = image_utils.generate_meme_image(
        meme_prompt=post_data["meme_prompt"],
        job_prefix=f"game_{today_str}",
    )
    if image_path:
        media_id = wp_client.upload_media(
            image_path=image_path,
            alt_text=post_data["meme_alt_text"],
        )
        print(f"[GAME] Meme image generated at {image_path}")

    # 6. 워드프레스에 이미지 업로드
    media_id = wp_client.upload_media(
        image_path=image_path,
        alt_text=post_data["meme_alt_text"],
    )
    print(f"[KR_TECH] Uploaded media. media_id={media_id}")

    # 7. 워드프레스에 글 발행
    wp_client.create_post(
        title=post_data["title"],
        body_markdown=post_data["body_markdown"],
        cynical_comment=post_data["cynical_comment"],
        meme_media_id=media_id,
        category_id=WP_CATEGORY_KR_TECH,
    )
    print("[KR_TECH] Post created on WordPress")

    # 8. 중복 방지용 기록
    key = f"{picked['url']}|{today_str}"
    storage.mark_posted(NAMESPACE, key)
    print(f"[KR_TECH] Marked as posted: {key}")

    print("[KR_TECH] Job finished.")
