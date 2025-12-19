from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def pick_top_item(candidates, context: str) -> dict:
    """
    candidates: list of {
        "title": str,
        "summary": str,
        "url": str
    }
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

    idx = resp.choices[0].message.parsed["index"]
    return candidates[idx]


def build_post(item, tone: str) -> dict:
    """
    tone:
      - us_tech
      - kr_tech
      - game
    """

    tone_desc = {
        "us_tech": "미국 테크 업계, 실리콘밸리 시각, 냉소적이지만 똑똑한 테크 칼럼니스트처럼",
        "kr_tech": "한국 테크 업계, 규제/대기업/스타트업 씬을 잘 아는 냉소적인 한국 IT 칼럼니스트처럼",
        "game": "글로벌 게임 업계 분위기와 밈 문화를 이해하는 날카롭고 시니컬한 게임 기자처럼",
    }[tone]

    prompt = f"""
너는 {tone_desc} 글을 쓴다.

다음 뉴스 정보를 바탕으로 블로그 포스트용 데이터를 만들어라:

뉴스 제목: {item['title']}
뉴스 요약(있으면): {item.get('summary', '')}
원문 링크: {item['url']}

다음 형식(JSON, 반드시 준수):

{{
  "title": "블로그용 제목",
  "body_markdown": "3~6줄 정도의 요약. Markdown 형식 가능. 원문 링크도 포함.",
  "cynical_comment": "짧고 임팩트 있는 시니컬 코멘트 1줄",
  "meme_prompt": "이 뉴스에 어울리는 밈 이미지 설명 (AI 이미지 생성용)",
  "meme_alt_text": "ALT 텍스트"
}}
"""

    resp = client.chat.completions.create(
        model="gpt-5.1",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    return resp.choices[0].message.parsed
