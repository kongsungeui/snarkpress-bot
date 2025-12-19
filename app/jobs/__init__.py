# app/jobs/__init__.py
from .job_us_tech import run as run_us_tech
from .job_kr_tech import run as run_kr_tech
from .job_game_news import run as run_game_news

__all__ = ["run_us_tech", "run_kr_tech", "run_game_news"]
