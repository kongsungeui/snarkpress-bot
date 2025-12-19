# app/sources/news_kr.py
import feedparser
from typing import List, Dict

KR_TECH_FEEDS = [
    "https://feeds.feedburner.com/zdkorea",
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
    한국 IT/테크 뉴스 후보들을 여러 RSS에서 모아서 반환.
    """
    candidates: List[Dict[str, str]] = []

    for feed_url in KR_TECH_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"[news_kr] Failed to parse feed {feed_url}: {e}")
            continue

        for entry in parsed.entries[:limit_per_feed]:
            c = _entry_to_candidate(entry)
            if not c["title"] or not c["url"]:
                continue
            candidates.append(c)

    unique = {}
    for c in candidates:
        unique[c["url"]] = c

    return list(unique.values())
