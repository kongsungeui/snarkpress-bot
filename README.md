## ✅ `README.md`

```md
# 📰 SnarkPress Bot  
> "뉴스는 진지하게, 코멘트는 냉소적으로"  
> GPT + RSS + WordPress 자동 포스팅 봇

---

## 🔥 이게 뭐임?
`SnarkPress Bot`은 매일 정해진 시간에:

- 🇺🇸 **미국 테크 뉴스**
- 🇰🇷 **한국 테크 뉴스**
- 🎮 **글로벌 게임 뉴스**

각각에서 **가장 핫한 뉴스 1개를 자동으로 선택**하고,

- GPT로 요약/제목 생성
- 시니컬한 코멘트 생성
- 밈 이미지 자동 생성
- 워드프레스에 자동 포스팅

까지 풀 오토로 처리하는 봇입니다.

---

## 🏗️ 아키텍처 개요

```

RSS 뉴스 수집
↓
GPT가 오늘의 Top 뉴스 선택
↓
제목 + 요약 + 냉소 코멘트 생성
↓
밈 이미지 생성 (OpenAI Image API)
↓
워드프레스 포스팅 자동 발행

```

---

## 🧰 기술 스택

| 기능 | 기술 |
|------|------|
| 뉴스 수집 | RSS (feedparser) |
| AI 요약 / 코멘트 | OpenAI GPT |
| 이미지 | OpenAI Image |
| 블로그 발행 | WordPress REST API |
| 스케줄링 | PythonAnywhere Scheduled task |

---

## 📁 폴더 구조

```

snarkpress-bot/
├── README.md
├── requirements.txt
├── .env.example
├── run_us_tech.py
├── run_kr_tech.py
├── run_game_news.py
└── app/
├── config.py
├── common/
│   ├── gpt_utils.py
│   ├── image_utils.py
│   ├── wp_client.py
│   └── storage.py
├── sources/
│   ├── news_us.py
│   ├── news_kr.py
│   └── news_games.py
└── jobs/
├── job_us_tech.py
├── job_kr_tech.py
└── job_game_news.py

````

---

## 🚀 설치 & 실행

### 1️⃣ Clone repository

```bash
git clone https://github.com/YOU/snarkpress-bot.git
cd snarkpress-bot
````

---

### 2️⃣ 가상환경 생성 & 라이브러리 설치

```bash
pip install -r requirements.txt
```

---

### 3️⃣ `.env` 설정

`.env.example` 참고해서 `.env` 생성

```env
OPENAI_API_KEY=sk-...

WP_URL=https://your-wordpress-site.com
WP_USER=botuser
WP_APP_PASSWORD=xxxxx

WP_CAT_US_TECH=3
WP_CAT_KR_TECH=4
WP_CAT_GAME=5
```

> ⚠️ WordPress → 사용자 설정에서 Application Password 생성 필요

---

## 🧪 수동 테스트

아무거나 하나 실행해서 잘 되는지 확인

```bash
python run_us_tech.py
```

---

## ⏰ PythonAnywhere 스케줄 설정

**Scheduled Tasks**에서 다음처럼 등록:

| 시간 (KST) | 작업                 |
| -------- | ------------------ |
| 12:00    | `run_us_tech.py`   |
| 18:00    | `run_kr_tech.py`   |
| 00:00    | `run_game_news.py` |

PythonAnywhere는 UTC 기준이므로 KST → UTC 변환해서 넣어야 함.

---

## 🛡️ 안전장치

* 하루에 같은 기사 중복 발행 방지
* RSS 하나 죽어도 나머지 정상 동작
* GPT 실패하면 graceful exit
* 이미지 생성 실패 시 글이라도 발행 가능하도록 설계 가능

---

## 💡 커스터마이징 팁

### RSS 소스 수정

`app/sources/news_*.py` 수정하면 됨

### 냉소 톤 바꾸기

`gpt_utils.build_post()` 프롬프트 수정

### 포스트 포맷 수정

`wp_client.create_post()` 수정

---

## 😎 결과물 예시

* 제목
* 3~6줄 정도의 요약 (Markdown 가능)
* 짧고 똑똑한 냉소 코멘트 한 줄
* 귀찮음이 자동화된 밈 이미지 1장

---

## 🧷 To-Do (언젠가)

* [ ] 태그 자동 생성
* [ ] 댓글 AI 자동 생성 (지옥 시작 버튼)
* [ ] 트위터/X 자동 공유
* [ ] 텔레그램/디스코드 푸시봇 연동

---

## 🥂 목적

귀찮은 건 AI가 대신 하고,
우리는 그냥 구경하면서 실실 웃자.

---

## 🧑‍💻 Author

Made with equal parts caffeine + cynicism ☕️

```