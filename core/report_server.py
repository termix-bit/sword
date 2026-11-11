import secrets
import shutil
import subprocess
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from core.paths import REPORTS_DIR

def open_html_report(report_path):
    report_path = Path(report_path).resolve(strict=True)
    reports_root = Path(REPORTS_DIR).resolve()
    
    if not report_path.is_file() or report_path.suffix.lower() != ".html" or report_path.parent != reports_root:
        raise ValueError("Invalid HTML report path")

    html_data = report_path.read_bytes()
    token = secrets.token_urlsafe(32)
    served = threading.Event()

    class ReportHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != f"/{token}":
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(html_data)
            served.set()

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportHandler)
    port = server.server_address[1]

    def run_server():
        server.serve_forever()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    opener = shutil.which("termux-open-url")
    if not opener:
        server.shutdown()
        server.server_close()
        raise RuntimeError("termux-open-url not found")

    url = f"http://127.0.0.1:{port}/{token}"
    try:
        result = subprocess.run([opener, url], shell=False, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            raise RuntimeError(result.stderr or "Failed to open browser")
        if not served.wait(timeout=45):
            raise TimeoutError("Browser did not load HTML report")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
