# Mohamed-Inc

This project provides a very small command line tool to manage user accounts.

Features:
- Create a new user account.
- Access the admin panel using a single password.

The first time you run the application it creates a default admin
account with username `admin` and password `admin` for command line
use. The web interface no longer has a login page and instead requires
the password `258963` to access the dashboard.

## Running

You can either use the command line tool or the lightweight web interface.

To start the web interface run:

```bash
python3 server.py
```

Then open `http://localhost:8000` in your browser. Enter the password
`258963` to access the admin panel where you can create or delete
accounts.

Alternatively execute the script with Python 3:

```bash
python3 main.py
```

Follow the on-screen menu to create accounts or login. When logged in as
`admin` you can list or delete user accounts.
