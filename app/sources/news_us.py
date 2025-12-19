# app/sources/news_us.py
import feedparser
from typing import List, Dict

US_TECH_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/category/business/latest/rss",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
]


def _entry_to_candidate(entry) -> Dict[str, str]:
    title = getattr(entry, "title", "").strip()
    summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
    summary = summary.strip()
    link = getattr(entry, "link", "").strip()

    return {
        "title": title,
        "summary": summary,
        "url": link,
    }


def fetch_candidates(limit_per_feed: int = 5) -> List[Dict[str, str]]:
    """
    미국 테크 뉴스 후보들을 여러 RSS에서 모아서 반환.
    """
    candidates: List[Dict[str, str]] = []

    for feed_url in US_TECH_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            # 피드 하나 죽었다고 전체가 죽을 필요는 없음
            print(f"[news_us] Failed to parse feed {feed_url}: {e}")
            continue

        for entry in parsed.entries[:limit_per_feed]:
            c = _entry_to_candidate(entry)
            if not c["title"] or not c["url"]:
                continue
            candidates.append(c)

    # URL 기준으로 중복 제거
    unique = {}
    for c in candidates:
        unique[c["url"]] = c

    return list(unique.values())
