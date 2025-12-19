# 📰 SnarkPress Bot

> "뉴스는 진지하게, 코멘트는 냉소적으로"
> GPT + RSS + WordPress 자동 포스팅 봇

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![WordPress](https://img.shields.io/badge/WordPress-REST%20API-21759b.svg)](https://wordpress.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 목차

- [소개](#-소개)
- [주요 기능](#-주요-기능)
- [아키텍처](#-아키텍처)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 방법](#-설치-방법)
- [사용 방법](#-사용-방법)
- [스케줄링 설정](#-스케줄링-설정)
- [커스터마이징](#-커스터마이징)
- [트러블슈팅](#-트러블슈팅)
- [라이선스](#-라이선스)

---

## 🔥 소개

`SnarkPress Bot`은 RSS 피드에서 매일 가장 핫한 뉴스를 자동으로 선별하고, GPT로 요약 및 냉소적인 코멘트를 생성한 후, 밈 이미지와 함께 WordPress 블로그에 자동으로 포스팅하는 봇입니다.

### 처리하는 뉴스 카테고리

- 🇺🇸 **미국 테크 뉴스** - TechCrunch, The Verge, Ars Technica 등
- 🇰🇷 **한국 테크 뉴스** - 주요 IT 미디어
- 🎮 **글로벌 게임 뉴스** - 게임 관련 뉴스 소스

---

## ✨ 주요 기능

- 🤖 **AI 기반 뉴스 선별**: GPT가 여러 RSS 피드에서 가장 흥미로운 뉴스 자동 선택
- 📝 **자동 요약 생성**: 긴 기사를 3-6줄로 압축 요약
- 😏 **냉소적 코멘트**: 뉴스에 대한 위트있고 시니컬한 한줄 코멘트 생성
- 🎨 **밈 이미지 생성**: OpenAI Image API로 관련 밈 이미지 자동 생성
- 📰 **WordPress 자동 발행**: REST API를 통한 원클릭 포스팅
- 🔄 **중복 방지**: 같은 기사 재발행 방지 메커니즘
- ⏰ **스케줄링 지원**: 원하는 시간에 자동 실행
- 🛡️ **안정성**: Graceful degradation (한 소스 실패 시에도 계속 동작)

---

## 🏗️ 아키텍처

```
RSS 뉴스 수집 (feedparser)
          ↓
GPT가 오늘의 Top 뉴스 선택
          ↓
제목 + 요약 + 냉소 코멘트 생성
          ↓
밈 이미지 생성 (OpenAI Image API)
          ↓
WordPress 포스팅 자동 발행
```

---

## 🧰 기술 스택

| 기능 | 기술 |
|------|------|
| 뉴스 수집 | RSS (feedparser) |
| AI 요약 / 코멘트 | OpenAI GPT-4 |
| 이미지 생성 | OpenAI DALL-E |
| 이미지 처리 | Pillow |
| 블로그 발행 | WordPress REST API |
| 환경 변수 관리 | python-dotenv |
| 스케줄링 | PythonAnywhere / Cron |

---

## 📁 프로젝트 구조

```
snarkpress-bot/
├── README.md                    # 프로젝트 문서
├── requirements.txt             # Python 의존성
├── .env.example                 # 환경 변수 예시 (생성 필요)
├── run_us_tech.py              # 미국 테크 뉴스 실행 스크립트
├── run_kr_tech.py              # 한국 테크 뉴스 실행 스크립트
├── run_game_news.py            # 게임 뉴스 실행 스크립트
└── app/
    ├── config.py               # 설정 관리
    ├── common/                 # 공통 유틸리티
    │   ├── gpt_utils.py       # GPT API 헬퍼
    │   ├── image_utils.py     # 이미지 생성 및 처리
    │   ├── wp_client.py       # WordPress API 클라이언트
    │   └── storage.py         # 중복 방지 스토리지
    ├── sources/               # RSS 소스 정의
    │   ├── news_us.py        # 미국 뉴스 소스
    │   ├── news_kr.py        # 한국 뉴스 소스
    │   └── news_games.py     # 게임 뉴스 소스
    └── jobs/                  # 작업 로직
        ├── job_us_tech.py    # 미국 뉴스 작업
        ├── job_kr_tech.py    # 한국 뉴스 작업
        └── job_game_news.py  # 게임 뉴스 작업
```

---

## 🚀 설치 방법

### 필수 요구사항

- Python 3.8 이상
- OpenAI API Key (GPT-4 및 DALL-E 접근 권한)
- WordPress 사이트 및 Application Password

### 1️⃣ 저장소 클론

```bash
git clone https://github.com/kongsungeui/snarkpress-bot.git
cd snarkpress-bot
```

### 2️⃣ 가상환경 생성 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ 의존성 설치

```bash
pip install -r requirements.txt
```

### 4️⃣ 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 작성하세요:

```env
# OpenAI API 설정
OPENAI_API_KEY=sk-your-api-key-here

# WordPress 설정
WP_URL=https://your-wordpress-site.com
WP_USER=your-bot-username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx

# WordPress 카테고리 ID
WP_CAT_US_TECH=3
WP_CAT_KR_TECH=4
WP_CAT_GAME=5
```

> ⚠️ **WordPress Application Password 생성 방법**:
> 1. WordPress 관리자 → 사용자 → 프로필
> 2. "Application Passwords" 섹션에서 새 비밀번호 생성
> 3. 생성된 비밀번호를 공백 포함하여 복사

---

## 🧪 사용 방법

### 수동 실행 (테스트)

각 스크립트를 개별적으로 실행하여 테스트할 수 있습니다:

```bash
# 미국 테크 뉴스 포스팅
python run_us_tech.py

# 한국 테크 뉴스 포스팅
python run_kr_tech.py

# 게임 뉴스 포스팅
python run_game_news.py
```

### 출력 예시

```
🔍 RSS 피드에서 뉴스 수집 중...
✅ 15개 기사 발견
🤖 GPT로 최고의 뉴스 선택 중...
📝 요약 및 코멘트 생성 중...
🎨 밈 이미지 생성 중...
📰 WordPress에 포스팅 중...
✅ 포스팅 완료: https://your-site.com/post-url
```

---

## ⏰ 스케줄링 설정

### PythonAnywhere 사용 시

**Tasks** 메뉴에서 다음과 같이 설정:

| UTC 시간 | KST 시간 | 명령어 |
|---------|---------|-------|
| 03:00   | 12:00   | `python /home/username/snarkpress-bot/run_us_tech.py` |
| 09:00   | 18:00   | `python /home/username/snarkpress-bot/run_kr_tech.py` |
| 15:00   | 00:00   | `python /home/username/snarkpress-bot/run_game_news.py` |

> 💡 PythonAnywhere는 UTC 기준이므로 한국 시간(KST)에서 -9시간 적용

### Cron 사용 시 (Linux/macOS)

```bash
crontab -e
```

다음 라인 추가:

```cron
0 3 * * * cd /path/to/snarkpress-bot && /path/to/venv/bin/python run_us_tech.py
0 9 * * * cd /path/to/snarkpress-bot && /path/to/venv/bin/python run_kr_tech.py
0 15 * * * cd /path/to/snarkpress-bot && /path/to/venv/bin/python run_game_news.py
```

---

## 💡 커스터마이징

### RSS 소스 변경

`app/sources/news_*.py` 파일에서 RSS 피드 URL 수정:

```python
FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    # 여기에 원하는 RSS 추가
]
```

### 코멘트 톤 조정

`app/common/gpt_utils.py`의 `build_post()` 함수에서 프롬프트 수정:

```python
# 냉소적 톤을 유머러스하거나 중립적으로 변경 가능
system_prompt = "당신은 뉴스를 재치있게 요약하는 블로거입니다..."
```

### 포스트 포맷 변경

`app/common/wp_client.py`의 `create_post()` 함수에서 HTML 구조 수정 가능

### 이미지 스타일 변경

`app/common/image_utils.py`에서 이미지 생성 프롬프트 및 크기 조정

---

## 🛡️ 안전장치

- ✅ **중복 방지**: `storage.py`를 통해 이미 포스팅된 기사 URL 추적
- ✅ **Graceful Degradation**: 하나의 RSS 소스 실패 시 다른 소스로 계속 진행
- ✅ **에러 핸들링**: API 실패 시 적절한 로깅 및 종료
- ✅ **이미지 생성 선택적**: 이미지 생성 실패해도 텍스트 포스트는 발행 가능

---

## 🐛 트러블슈팅

### OpenAI API 오류

```
Error: OpenAI API key not found
```

**해결방법**: `.env` 파일에 `OPENAI_API_KEY`가 올바르게 설정되었는지 확인

### WordPress 인증 실패

```
Error: 401 Unauthorized
```

**해결방법**:
1. WordPress Application Password가 올바른지 확인
2. `WP_USER`가 실제 사용자명(이메일 아님)인지 확인
3. WordPress REST API가 활성화되어 있는지 확인

### RSS 피드 읽기 실패

```
Error: Failed to fetch RSS feed
```

**해결방법**:
1. 인터넷 연결 확인
2. RSS 피드 URL이 유효한지 브라우저에서 테스트
3. `app/sources/` 파일에서 피드 URL 확인

### 이미지 생성 실패

```
Error: Image generation failed
```

**해결방법**:
1. OpenAI API 크레딧 잔액 확인
2. 이미지 생성 프롬프트가 OpenAI 정책에 부합하는지 확인
3. 필요 시 `image_utils.py`에서 이미지 생성 스킵 옵션 추가

---

## 🧷 로드맵

향후 개선 계획:

- [ ] 태그 자동 생성
- [ ] 다중 WordPress 사이트 지원
- [ ] 트위터/X 자동 공유
- [ ] 텔레그램/디스코드 알림 봇 연동
- [ ] 웹 대시보드 (Flask/Streamlit)
- [ ] 포스팅 통계 및 분석

---

## 🥂 철학

귀찮은 건 AI가 대신하고,
우리는 그냥 구경하면서 실실 웃는다.

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 🧑‍💻 제작자

Made with equal parts caffeine + cynicism ☕️💭

**기여하기**: 이슈나 PR은 언제나 환영합니다!

---

## 📞 문의

- Issues: [GitHub Issues](https://github.com/kongsungeui/snarkpress-bot/issues)
- Discussions: [GitHub Discussions](https://github.com/kongsungeui/snarkpress-bot/discussions)

---

**⭐️ 이 프로젝트가 유용하다면 Star를 눌러주세요!**
