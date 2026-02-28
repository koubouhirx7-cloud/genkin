import http.server
import socketserver
import json
import os
from http import cookies

# Load .env manually
env_file = '.env'
env_vars = {}
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                env_vars[k.strip()] = v.strip()

PIN_CODE = env_vars.get('APP_PIN', '8888')
PORT = 8085

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Prevent caching of HTML
        if self.path.endswith('.html') or self.path == '/':
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        # Serve login.html without auth
        if self.path == '/login.html' or not self.path.endswith('.html'):
            if self.path == '/':
                self.path = '/login.html'
            super().do_GET()
            return
            
        # Check cookie for HTML files
        cookie_header = self.headers.get('Cookie', '')
        c = cookies.SimpleCookie(cookie_header)
        auth_cookie = c.get('session')
        
        if auth_cookie and auth_cookie.value == 'authenticated':
            super().do_GET()
        else:
            self.send_response(302)
            self.send_header('Location', '/login.html')
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_data)
                pin = data.get('pin')
            except:
                pin = None
            
            if pin == PIN_CODE:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Set-Cookie', 'session=authenticated; Path=/; HttpOnly; SameSite=Lax; Max-Age=86400')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
            else:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False}).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

with socketserver.TCPServer(("", PORT), AuthHandler) as httpd:
    print(f"Secure server started on port {PORT}")
    print(f"Uses PIN code from .env: '{PIN_CODE}'")
    print(f"Access point: http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
