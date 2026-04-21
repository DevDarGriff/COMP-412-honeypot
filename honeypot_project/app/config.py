from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "events.jsonl"

HOST = "127.0.0.1"

HTTP_PORT = 8080
SSH_PORT = 2222
TELNET_PORT = 2323

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

COMMON_ATTACK_USERNAMES = {
    "root",
    "admin",
    "administrator",
    "test",
    "guest",
    "user",
    "oracle",
    "ubuntu",
}

REPEAT_ATTEMPT_THRESHOLD = 5
SSH_BANNER = "SSH-2.0-OpenSSH_8.21 Ubuntu-4ubuntu0.5\r\n"
TELNET_BANNER = "Ubuntu 20.04 LTS\r\n"
