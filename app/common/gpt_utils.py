import json
from html import escape
from typing import List, Dict

from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def _extract_text_content(message) -> str:
    """
    OpenAI SDK v1 기준:
    - message.content 가 리스트(TextContentBlock[]) 일 수 있어서
      그걸 전부 합쳐서 하나의 문자열로 만든다.
    """
    content = message.content
    if isinstance(content, str):
        return content

    # content 가 list 인 경우 (멀티 파트)
    parts = []
    for part in content:
        # TextContentBlock 인 경우 .text 존재
        text = getattr(part, "text", None)
        if text is None:
            # 혹시 모를 fallback
            if isinstance(part, str):
                text = part
            else:
                text = ""
        parts.append(text)
    return "".join(parts)


def pick_top_item(candidates: List[Dict[str, str]], context: str) -> Dict[str, str]:
    """
    candidates: list of {
        "title": str,
        "summary": str,
        "url": str
    }

    반환: 선택된 candidate 하나
    """
    if not candidates:
        raise ValueError("No news candidates provided")

    text = ""
    for i, c in enumerate(candidates):
        text += f"[{i}] {c['title']}\n"
        text += f"URL: {c['url']}\n"
        text += f"요약: {c.get('summary', '')}\n\n"

    prompt = f"""
다음은 뉴스 후보 목록이다.

{context}

{text}

위 목록 중에서 오늘 블로그에 올리기 가장 적합한 뉴스 하나만 선택해라.
기준:
- 파급력
- 대중적 관심
- 트렌드 반영
- 오늘이라는 '타이밍'에 맞는 이슈

출력 형식 (반드시 JSON):
{{"index": 숫자}}
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    raw = _extract_text_content(resp.choices[0].message)
    data = json.loads(raw)

    idx = data["index"]
    return candidates[idx]


def build_post(item: Dict[str, str], tone: str) -> Dict[str, str]:
    """
    tone:
      - us_tech
      - kr_tech
      - game

    반환 예:
    {
      "title": "...",
      "body_markdown": "...",
      "cynical_comment": "...",
      "meme_prompt": "...",
      "meme_alt_text": "...",
      "source_link_text": "..."
    }
    """

    tone_desc_map = {
        "us_tech": "미국 테크 업계, 실리콘밸리 시각, 냉소적이지만 똑똑한 테크 칼럼니스트처럼",
        "kr_tech": "한국 테크 업계, 규제/대기업/스타트업 씬을 잘 아는 냉소적인 한국 IT 칼럼니스트처럼",
        "game": "글로벌 게임 업계 분위기와 밈 문화를 이해하는 날카롭고 시니컬한 게임 기자처럼",
    }
    tone_desc = tone_desc_map.get(tone, "냉소적인 테크 칼럼니스트처럼")

    prompt = f"""
너는 {tone_desc} 글을 쓴다.

다음 뉴스 정보를 바탕으로 블로그 포스트용 데이터를 만들어라:

뉴스 제목: {item['title']}
뉴스 요약(있으면): {item.get('summary', '')}
원문 링크: {item['url']}

다음 형식(JSON, 반드시 준수):

{{
  "title": "블로그용 제목",
  "body_markdown": "3~6줄 정도의 요약. Markdown 형식 가능. 원문 링크는 넣지 말고 본문만",
  "cynical_comment": "짧고 임팩트 있는 시니컬 코멘트 1줄",
  "meme_prompt": "이 뉴스에 어울리는 밈 이미지 설명 (AI 이미지 생성용)",
  "meme_alt_text": "ALT 텍스트",
  "source_link_text": "원문 링크용 앵커 텍스트 (간결하게)"
}}
"""

    resp = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    raw = _extract_text_content(resp.choices[0].message)
    data = json.loads(raw)

    return data


def append_source_link(body_markdown: str, source_url: str, link_text: str = "원문 보기") -> str:
    """
    본문 마크다운에 원문 링크 HTML 블록을 덧붙인다.
    - body_markdown: GPT가 생성한 본문(링크 없음)
    - source_url: 원문 URL
    - link_text: 앵커 텍스트(없으면 기본값)
    """

    if not source_url:
        return body_markdown

    safe_url = escape(source_url, quote=True)
    safe_text = escape(link_text or "원문 보기")
    source_block = f'<p><strong>원문:</strong> <a href="{safe_url}">{safe_text}</a></p>'

    if body_markdown.strip():
        return f"{body_markdown}\n\n{source_block}"
    return source_block
