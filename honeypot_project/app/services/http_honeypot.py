from flask import Flask, render_template, request, redirect, url_for
from app.logger import log_event
from app.detectors import classify_event
from pathlib import Path

#app = Flask(__name__)



BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

app = Flask(__name__, template_folder=str(TEMPLATES_DIR))

def get_source_ip() -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"



def base_event(event_type: str) -> dict:
    source_ip = get_source_ip()
    user_agent = request.headers.get("User-Agent", "")
    labels = classify_event(
        service="http",
        source_ip=source_ip,
        path=request.path,
        user_agent=user_agent,
        event_type=event_type
    )

    return {
        "service": "http",
        "event_type": event_type,
        "source_ip": source_ip,
        "method": request.method,
        "path": request.path,
        "query_string": request.query_string.decode("utf-8", errors="ignore"),
        "user_agent": user_agent,
        "labels": labels,
    }


@app.route("/", methods=["GET"])
def index():
    event = base_event("request")
    log_event(event)
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        event = base_event("request")
        log_event(event)
        return render_template("login.html", error=None)
    
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    event = base_event("login_attempt")
    event["username"] = username
    event["password"] = password
    log_event(event)

    return render_template("login.html", error="Invalid username or password."), 401


@app.route("/admin", methods=["GET"])
def admin():
    event = base_event("request")
    log_event(event)
    return render_template("admin.html"), 403


@app.route("/phpmyadmin", methods=["GET"])
def phpmyadmin():
    event = base_event("request")
    log_event(event)
    return "Access denied.", 403

@app.route("/wp-admin", methods=["GET"])
def wp_admin():
    event = base_event("request")
    log_event(event)
    return redirect(url_for("login"))


@app.errorhandler(404)
def not_found(error):
    event = base_event("not_found")
    log_event(event)
    return "404: Not Found.", 404

