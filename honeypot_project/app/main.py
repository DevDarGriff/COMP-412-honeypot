import threading
from app.config import HOST, HTTP_PORT, SSH_PORT, TELNET_PORT, DEBUG
from app.services.http_honeypot import app
from app.services.ssh_honeypot import start_ssh_server
from app.services.telnet_honeypot import start_telnet_server

def run_ssh():
    ssh_server = start_ssh_server(HOST, SSH_PORT)
    print(f"[+] SSH honeypot listening on {HOST}:{SSH_PORT}")
    ssh_server.serve_forever()

def run_telnet():
    telnet_server = start_telnet_server(HOST, TELNET_PORT)
    print(f"[+] Telnet honeypot listening on {HOST}:{TELNET_PORT}")
    telnet_server.serve_forever()

if __name__ == "__main__":
    ssh_thread = threading.Thread(target=run_ssh, daemon=True)
    telnet_thread = threading.Thread(target=run_telnet, daemon=True)

    ssh_thread.start()
    telnet_thread.start()

    print(f"[+] HTTP honeypot listening on {HOST}:{HTTP_PORT}")
    app.run(host=HOST, port=HTTP_PORT, debug=DEBUG, use_reloader=False)
