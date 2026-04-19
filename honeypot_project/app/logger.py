import json
from datetime import datetime, timezone
from app.config import LOG_FILE


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(event: dict) -> None:
    event = dict(event)
    event["timestamp"] = utc_now_iso()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")