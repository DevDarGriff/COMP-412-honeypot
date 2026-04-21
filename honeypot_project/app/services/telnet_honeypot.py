import socketserver
from app.config import TELNET_BANNER
from app.logger import log_event
from app.detectors import classify_event

class TelnetHandler(socketserver.BaseRequestHandler):
    def handle(self):
        source_ip = self.client_address[0]

        log_event({
            "service": "telnet",
            "event_type": "connection",
            "source_ip": source_ip,
            "port": self.client_address[1],
            "labels": classify_event(
                service="telnet",
                source_ip=source_ip,
                event_type="connection",
            ),
        })

        try:
            self.request.sendall(TELNET_BANNER.encode("utf-8"))
            self.request.sendall(b"login: ")
            username = self._recv_line()

            self.request.sendall(b"Password: ")
            password = self._recv_line()

            labels = classify_event(
                service="telnet",
                source_ip=source_ip,
                event_type="telnet_auth_attempt",
                username=username,
            )

            log_event({
                "service": "telnet",
                "event_type": "telnet_auth_attempt",
                "source_ip": source_ip,
                "username": username,
                "password": password,
                "labels": labels,
            })

            self.request.sendall(b"\r\nLogin incorrect\r\n")

        except Exception as e:
            log_event({
                "service": "telnet",
                "event_type": "error",
                "source_ip": source_ip,
                "error": str(e),
                "labels": ["service_error"],
            })

    def _recv_line(self, limit: int = 1024) -> str:
        data = b""
        while len(data) < limit:
            chunk = self.request.recv(1)
            if not chunk:
                break
            if chunk in (b"\n", b"\r"):
                break
            data += chunk
        return data.decode("utf-8", errors="ignore").strip()

class ThreadedTelnetServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

def start_telnet_server(host: str, port: int):
    server = ThreadedTelnetServer((host, port), TelnetHandler)
    return server