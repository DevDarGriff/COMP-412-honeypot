# Local Python Honeypot for Web Reconnaissance and Credential Logging

## Overview

This project implements a **low-interaction honeypot** in Python designed to simulate a corporate internal web portal and capture suspicious activity such as:

* reconnaissance probing (e.g., `/admin`, `/phpmyadmin`)
* automated scanner traffic (e.g., `sqlmap`, `nikto`)
* credential guessing attempts
* repeated access patterns from a single source

---

## Key Concepts

### Low-Interaction Honeypot

This system simulates services (HTTP endpoints) without providing a real backend or shell access. It is safer and easier to control than high-interaction honeypots.

### Structured Logging

All events are stored as **JSON lines (`.jsonl`)**, making them easy to analyze and process.

### Rule-Based Detection

Activity is labeled using simple, explainable rules such as:

* `recon`
* `scanner`
* `credential_attack`
* `repeat_source`

---

## Project Structure

```text
honeypot_project/
├── app/
│   ├── main.py                # Entry point (starts Flask server)
│   ├── config.py              # Configuration (ports, rules, paths)
│   ├── logger.py              # JSON event logging
│   ├── detectors.py           # Classification logic
│   ├── report.py              # Summary report generator
│   └── services/
│       └── http_honeypot.py   # Flask routes / honeypot behavior
│
├── templates/
│   ├── index.html             # Landing page
│   ├── login.html             # Fake login page
│   └── admin.html             # Fake admin panel
│
├── static/
│   └── style.css              # UI styling
│
├── logs/
│   └── events.jsonl           # Captured event logs
│
├── requirements.txt
└── README.md
```

---

## Requirements

* Python **3.10+**
* pip

---

## How to Run

### 1. Clone or navigate to project

```bash
cd honeypot_project
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate virtual environment

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the honeypot

```bash
python3 -m app.main
```

### 6. Open in browser

```text
http://127.0.0.1:8080
```

---

## Testing the Honeypot

### Browser Interaction

* Visit `/`
* Navigate to `/login`
* Submit fake credentials
* Visit `/admin` or `/phpmyadmin`

### Simulated Attack Traffic (Terminal)

```text
In a second terminal (not running the honeypot), run the following commands:
```

```bash
curl http://127.0.0.1:8080/admin
curl http://127.0.0.1:8080/phpmyadmin
curl http://127.0.0.1:8080/wp-admin
curl http://127.0.0.1:8080/.env

curl -A "sqlmap/1.0" http://127.0.0.1:8080/login
curl -A "nikto/2.5.0" http://127.0.0.1:8080/admin

curl -X POST http://127.0.0.1:8080/login -d "username=admin&password=admin"
curl -X POST http://127.0.0.1:8080/login -d "username=root&password=toor"
```

---

## Generating a Report

After generating activity:

```bash
python3 -m app.report
```

### Example Output

```
HONEYPOT SUMMARY REPORT
----------------------------------------
Total events: 25
Login attempts: 5

Top requested paths:
  /admin: 6
  /login: 5

Top usernames:
  admin: 2
  root: 1

Labels:
  recon: 10
  scanner: 5
  credential_attack: 5
```

---

## Log Format

Each event is stored as a JSON object:

```json
{
  "timestamp": "2026-04-18T14:22:11Z",
  "service": "http",
  "event_type": "login_attempt",
  "source_ip": "127.0.0.1",
  "method": "POST",
  "path": "/login",
  "user_agent": "curl/8.5.0",
  "username": "admin",
  "password": "password123",
  "labels": ["credential_attack", "repeat_source"]
}
```

---

## Detection Labels

| Label               | Description                          |
| ------------------- | ------------------------------------ |
| `recon`             | Access to known sensitive paths      |
| `scanner`           | Suspicious user-agent detected       |
| `credential_attack` | Login attempt submitted              |
| `repeat_source`     | High frequency requests from same IP |
| `generic_activity`  | Normal interaction                   |

---

## License

This project is licensed under the [MIT] License - see the [LICENSE](LICENSE.txt) file for details.