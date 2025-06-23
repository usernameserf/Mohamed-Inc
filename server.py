from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import uuid
from http.cookies import SimpleCookie
from main import load_users, save_users, hash_password, create_account, ensure_admin

ADMIN_PASSWORD = "258963"

sessions = {}

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200, headers=None):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_session_user(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return None
        cookie = SimpleCookie()
        cookie.load(cookie_header)
        token = cookie.get('session')
        if not token:
            return None
        return sessions.get(token.value)

    def _require_admin(self):
        user = self._get_session_user()
        if user != 'admin':
            self.send_response(403)
            self.end_headers()
            return False
        return True

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            with open('index.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
        elif self.path == '/users':
            if not self._require_admin():
                return
            users = load_users()
            self._send_json(users)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        data = json.loads(body or '{}')

        if self.path == '/auth':
            password = data.get('password')
            if password == ADMIN_PASSWORD:
                token = uuid.uuid4().hex
                sessions[token] = 'admin'
                headers = {'Set-Cookie': f'session={token}; HttpOnly; Path=/'}
                self._send_json({'message': 'Access granted.'}, headers=headers)
            else:
                self._send_json({'message': 'Invalid password.'}, status=401)
        elif self.path == '/create':
            if not self._require_admin():
                return
            username = data.get('username')
            password = data.get('password')
            create_account(username, password)
            self._send_json({'status': 'ok'})
        elif self.path == '/delete':
            if not self._require_admin():
                return
            username = data.get('username')
            users = load_users()
            if username in users and username != 'admin':
                del users[username]
                save_users(users)
            self._send_json({'status': 'ok'})
        elif self.path == '/logout':
            token = None
            cookie_header = self.headers.get('Cookie')
            if cookie_header:
                cookie = SimpleCookie()
                cookie.load(cookie_header)
                token_cookie = cookie.get('session')
                if token_cookie:
                    token = token_cookie.value
            if token:
                sessions.pop(token, None)
            headers = {'Set-Cookie': 'session=; Max-Age=0; Path=/; HttpOnly'}
            self._send_json({'message': 'Logged out'}, headers=headers)
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=Handler):
    ensure_admin()
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Server running at http://localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
