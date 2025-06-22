from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from main import load_users, save_users, hash_password, create_account, ensure_admin

current_user = None

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            with open('index.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
        elif self.path == '/users':
            if current_user != 'admin':
                self.send_response(403)
                self.end_headers()
                return
            users = load_users()
            self._send_json(users)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global current_user
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        data = json.loads(body or '{}')

        if self.path == '/login':
            username = data.get('username')
            password = data.get('password')
            users = load_users()
            user = users.get(username)
            if user and user['password'] == hash_password(password):
                current_user = username
                self._send_json({'message': 'Login successful.', 'admin': user.get('is_admin', False)})
            else:
                self._send_json({'message': 'Invalid credentials.', 'admin': False}, status=401)
        elif self.path == '/register':
            username = data.get('username')
            password = data.get('password')
            users = load_users()
            if username in users:
                self._send_json({'message': 'User already exists.'}, status=400)
            else:
                create_account(username, password)
                self._send_json({'message': 'Account created.'})
        elif self.path == '/create':
            if current_user != 'admin':
                self.send_response(403)
                self.end_headers()
                return
            username = data.get('username')
            password = data.get('password')
            create_account(username, password)
            self._send_json({'status': 'ok'})
        elif self.path == '/delete':
            if current_user != 'admin':
                self.send_response(403)
                self.end_headers()
                return
            username = data.get('username')
            users = load_users()
            if username in users and username != 'admin':
                del users[username]
                save_users(users)
            self._send_json({'status': 'ok'})
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
