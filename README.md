# Mohamed-Inc

This project provides a very small command line tool to manage user accounts.

Features:
- Create a new user account.
- Login as a regular user.
- Login as an admin user and manage all accounts.

The first time you run the application it creates a default admin
account with username `admin` and password `admin`.

## Running

You can either use the command line tool or the lightweight web interface.

To start the web interface run:

```bash
python3 server.py
```

Then open `http://localhost:8000` in your browser. Admin users can create or delete accounts from the admin panel.

Alternatively execute the script with Python 3:

```bash
python3 main.py
```

Follow the on-screen menu to create accounts or login. When logged in as
`admin` you can list or delete user accounts.
