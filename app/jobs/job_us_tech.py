# app/jobs/job_us_tech.py
from datetime import date

from app.sources import news_us
from app.common import gpt_utils, image_utils, wp_client, storage
from app.config import WP_CATEGORY_US_TECH


NAMESPACE = "us_tech"


def run():
    today_str = date.today().isoformat()
    print(f"[US_TECH] Job start for {today_str}")

    # 1. 후보 뉴스 수집
    candidates = news_us.fetch_candidates(limit_per_feed=5)
    print(f"[US_TECH] Fetched {len(candidates)} candidates (before filtering)")

    # 2. 오늘 이미 올린 URL은 제외
    filtered = []
    for c in candidates:
        key = f"{c['url']}|{today_str}"
        if storage.is_posted(NAMESPACE, key):
            print(f"[US_TECH] Skip already posted: {c['url']}")
            continue
        filtered.append(c)

    if not filtered:
        print("[US_TECH] No new candidates after filtering. Exit.")
        return

    print(f"[US_TECH] {len(filtered)} candidates after filtering")

    # 3. GPT로 오늘의 뉴스 하나 선택
    picked = gpt_utils.pick_top_item(
        filtered,
        context="미국 테크/실리콘밸리 뉴스 중 오늘 가장 임팩트 있는 뉴스를 하나 골라라.",
    )
    print(f"[US_TECH] Picked: {picked['title']}")

    # 4. GPT로 포스팅 데이터 생성
    post_data = gpt_utils.build_post(picked, tone="us_tech")
    print("[US_TECH] Post data generated from GPT")

    # 5. 밈 이미지 생성
    image_path = image_utils.generate_meme_image(
        meme_prompt=post_data["meme_prompt"],
        job_prefix=f"us_tech_{today_str}",
    )
    print(f"[US_TECH] Meme image generated at {image_path}")

    # 6. 워드프레스에 이미지 업로드
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
        
    # 7. 워드프레스에 글 발행
    body_with_source = gpt_utils.append_source_link(
        body_markdown=post_data["body_markdown"],
        source_url=picked["url"],
        link_text=post_data.get("source_link_text", "원문 보기"),
    )

    wp_client.create_post(
        title=post_data["title"],
        body_markdown=body_with_source,
        cynical_comment=post_data["cynical_comment"],
        meme_media_id=media_id,
        category_id=WP_CATEGORY_US_TECH,
    )
    print("[US_TECH] Post created on WordPress")

    # 8. 중복 방지용 기록
    key = f"{picked['url']}|{today_str}"
    storage.mark_posted(NAMESPACE, key)
    print(f"[US_TECH] Marked as posted: {key}")

    print("[US_TECH] Job finished.")
