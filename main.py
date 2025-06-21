import json
import hashlib
import os

DB_FILE = 'users.json'


def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def ensure_admin():
    users = load_users()
    if 'admin' not in users:
        print('Creating default admin account: username=admin password=admin')
        users['admin'] = {
            'password': hash_password('admin'),
            'is_admin': True
        }
        save_users(users)


def create_account(username: str, password: str, is_admin: bool = False):
    users = load_users()
    if username in users:
        print('User already exists.')
        return
    users[username] = {
        'password': hash_password(password),
        'is_admin': is_admin
    }
    save_users(users)
    print('Account created for', username)


def login(username: str, password: str):
    users = load_users()
    user = users.get(username)
    if user and user['password'] == hash_password(password):
        print('Login successful.')
        return user
    print('Invalid credentials.')
    return None


def admin_panel():
    while True:
        print('\nAdmin panel:')
        print('1) List accounts')
        print('2) Delete account')
        print('3) Logout')
        choice = input('Select: ')
        if choice == '1':
            users = load_users()
            for name, info in users.items():
                print(f"{name} (admin: {info['is_admin']})")
        elif choice == '2':
            user_to_delete = input('User to delete: ')
            users = load_users()
            if user_to_delete in users:
                if user_to_delete == 'admin':
                    print('Cannot delete default admin.')
                    continue
                del users[user_to_delete]
                save_users(users)
                print('User deleted.')
            else:
                print('User not found.')
        elif choice == '3':
            break
        else:
            print('Invalid option.')


def main():
    ensure_admin()
    while True:
        print('\nMenu:')
        print('1) Create account')
        print('2) Login')
        print('3) Quit')
        choice = input('Select: ')
        if choice == '1':
            username = input('New username: ')
            password = input('New password: ')
            create_account(username, password)
        elif choice == '2':
            username = input('Username: ')
            password = input('Password: ')
            user = login(username, password)
            if user and user.get('is_admin'):
                admin_panel()
        elif choice == '3':
            break
        else:
            print('Invalid option.')


if __name__ == '__main__':
    main()
