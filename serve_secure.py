import http.server
import socketserver
import base64
import sys

PORT = 8086
USER = "admin"
PASS = "1234"

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_authhead(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Secure Area"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        auth = self.headers.get('Authorization')
        if not auth:
            self.do_authhead()
            self.wfile.write(b"No auth header received")
            pass
        elif auth == 'Basic ' + base64.b64encode(f'{USER}:{PASS}'.encode('utf-8')).decode('ascii'):
            super().do_GET()
        else:
            self.do_authhead()
            self.wfile.write(b"Not authenticated")
            pass

Handler = AuthHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Basic Auth Server started on port {PORT}")
    print(f"Username: {USER}")
    print(f"Password: {PASS}")
    print("Access via your IP address from smartphone (e.g., http://192.168.x.x:8086)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
