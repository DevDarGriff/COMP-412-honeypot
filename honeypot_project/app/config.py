from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "events.jsonl"

HOST = "127.0.0.1"
PORT = 8080
DEBUG = True

SUSPICIOUS_PATHS = {
    "/admin",
    "/login",
    "/wp-admin",
    "/phpmyadmin",
    "/.env",
    "/config",
    "/server-status",
    "/backup",
    "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php",

}

SUSPICIOUS_USER_AGENTS = [
    "sqlmap",
    "nitko",
    "nmap",
    "masscan",
    "curl",
    "wget",
    "python-requests",
    "scanner",

]

REPEAT_ATTEMPT_THRESHOLD = 5
