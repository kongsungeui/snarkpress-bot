import json
from pathlib import Path
from datetime import date
from app.config import DATA_PATH


def _load():
    if not DATA_PATH.exists():
        return {}
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _save(data):
    DATA_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def is_posted(namespace: str, key: str) -> bool:
    """
    namespace:
      us_tech | kr_tech | game

    key:
      보통 -> f"{url}|{YYYY-MM-DD}"
    """

    data = _load()
    return data.get(namespace, {}).get(key, False)


def mark_posted(namespace: str, key: str):
    data = _load()
    ns = data.setdefault(namespace, {})
    ns[key] = str(date.today())
    _save(data)
