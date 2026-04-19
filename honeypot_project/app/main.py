from app.config import HOST, PORT, DEBUG
from app.services.http_honeypot import app

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)