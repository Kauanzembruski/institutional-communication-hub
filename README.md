# IFRS Institutional Board

A web application designed to centralize institutional communication: announcements, events, reminders, cafeteria menus, exams, upcoming classes, important dates, and lost-and-found items. It provides a public information dashboard, an authenticated management area, and Django Admin.

## Stack

| Layer | Technologies |
| --- | --- |
| Language | Python; local environment validated with Python 3.14 |
| Backend | Django 6.0.3, views, templates, and ORM |
| Database | PostgreSQL and psycopg2-binary |
| Cache | Redis and django-redis 7.0.0 |
| Request Rate Limiting | django-ratelimit 4.1.0 with Redis |
| Interface | HTML, CSS, and JavaScript with Django Templates |
| Configuration | python-decouple and `.env` environment variables |
| Static Files | Django Staticfiles and WhiteNoise middleware |
| External Integration | Open-Meteo, accessed with Requests for weather information |
| Authentication | Django sessions, authentication, and password recovery |
| Server Entry Points | WSGI and ASGI; Gunicorn included in dependencies for Linux |

Package versions are listed in [`requirements.txt`](requirements.txt). Local development uses Redis directly on Windows, without Docker. Additional libraries included in the dependencies do not necessarily represent active features.

## Features

- Public dashboard with institutional information and weather data.
- Authenticated area for content management and Django Admin.
- Institutional announcements, reminders, and operational information.
- Event calendar and important dates.
- Cafeteria menu and exam calendar.
- Upcoming class lookup by course/class group.
- Lost-and-found item registration with images.
- Password recovery by email.
- Request rate limiting for operations such as login, uploads, and deletions.

## Project Structure

```text
IFATUALIZADO/
├── institucional/       # Settings, URLs, WSGI, and ASGI
├── apps/
│   ├── core/            # Shared resources and request rate limiting
│   └── dashboard/       # Models and views for the board and management area
├── achadoseperdidos/    # Lost-and-found items
├── avisosinst/          # Institutional announcements
├── cardapio/            # Cafeteria menu
├── datasimport/         # Important dates
├── eventos/             # Events
├── infop/               # Operational information
├── lembretes/           # Reminders
├── provas/              # Exam calendar
├── pxaulas/             # Upcoming classes
├── templates/           # Pages and email templates
├── static/              # CSS, JavaScript, and interface images
├── docs/                # Documentation and historical references
├── .env.example         # Configuration template without credentials
├── manage.py
├── requirements.txt
├── start-redis.ps1      # Redis startup script for Windows
└── runserver.ps1        # Local environment startup script
```

## Prerequisites

- Git and Python 3.12 or later, compatible with Django 6. The commands below use Python 3.14, which has been validated locally.
- PostgreSQL accessible with a schema compatible with the project models.
- Redis. The local configuration uses `127.0.0.1:6380`, Redis database `1`.
- PowerShell for the Windows startup scripts.

## Installation on Windows

### 1. Clone the Repository and Create the Virtual Environment

```powershell
git clone https://github.com/Kauanzembruski/IFATUALIZADO.git
cd IFATUALIZADO
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Activating the virtual environment is optional when commands use the full Python path. To activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Configure the Environment

```powershell
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the generated key into `SECRET_KEY` and fill in the required credentials in `.env`.

| Variable | Purpose | Local Value |
| --- | --- | --- |
| `DEBUG` | Development mode | `True` |
| `SECRET_KEY` | Django secret key | Generate your own key |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | Fill in |
| `DB_USER` | Database user | Fill in |
| `DB_PASSWORD` | Database password | Fill in |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `REDIS_URL` | Cache connection | `redis://127.0.0.1:6380/1` |
| `EMAIL_BACKEND` | Email backend | Console backend in development |

For SMTP, also configure `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and, if necessary, `DEFAULT_FROM_EMAIL` and `SERVER_EMAIL`.

When using the console email backend, password recovery emails are displayed directly in the terminal.

### 3. Install Redis Without Docker

The script uses the community distribution [Redis 8.10.2 for Windows x64 Cygwin](https://github.com/redis-windows/redis-windows/releases/tag/8.10.2).

Download and extract it:

```powershell
New-Item -ItemType Directory -Path tools\redis -Force
Invoke-WebRequest 'https://github.com/redis-windows/redis-windows/releases/download/8.10.2/Redis-8.10.2-Windows-x64-cygwin.zip' -OutFile tools\redis.zip
Expand-Archive tools\redis.zip -DestinationPath tools\redis -Force
```

The resulting folder should be:

```text
tools\redis\Redis-8.10.2-Windows-x64-cygwin
```

Create a `redis-local.conf` file inside that directory with:

```conf
bind 127.0.0.1
protected-mode yes
port 6380
daemonize no
logfile redis-local.log
dir .
save ""
appendonly no
```

Start Redis and verify that it is working:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-redis.ps1
& .\tools\redis\Redis-8.10.2-Windows-x64-cygwin\redis-cli.exe -p 6380 ping
```

The expected response is:

```text
PONG
```

Redis runs in the background, restricted to the local machine, and is configured as a non-persistent cache.

Port `6380` is used to avoid conflicts with services running on the default Redis port `6379`.

The Redis executables are not version-controlled.

To stop Redis:

```powershell
& .\tools\redis\Redis-8.10.2-Windows-x64-cygwin\redis-cli.exe -p 6380 shutdown
```

### 4. Prepare PostgreSQL

The project combines Django-managed models with `managed = False` models linked to existing database tables.

Therefore, **`migrate` does not create all business-related tables**.

A PostgreSQL schema compatible with the current project models must be available before using the application.

If you have an authorized database backup, restore it separately. Database dumps and real production data are not included in the repository.

`docs/criar_banco_postgresql.txt` is a historical reference, not a complete installer for the current database schema.

It contains commands for deleting and recreating databases and tables. Review it carefully before using it and never run it against data you want to preserve.

Once the correct schema is available and the credentials are configured:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py check
```

### 5. Run the Application

```powershell
powershell -ExecutionPolicy Bypass -File .\runserver.ps1
```

The script:

- verifies that the required credentials are configured;
- starts Redis;
- runs Django system checks;
- starts the development server at `http://127.0.0.1:8000`.

| Route | Area |
| --- | --- |
| `/` | Public dashboard |
| `/home/` | Authenticated area entry point |
| `/home/painel/` | Management dashboard |
| `/admin/` | Django Admin |
| `/home/esqueci-senha/` | Password recovery |
| `/lembretePublico/` | Public reminders screen |

To use a different port:

```powershell
powershell -ExecutionPolicy Bypass -File .\runserver.ps1 -Address 127.0.0.1:8001
```

## Linux and macOS

Install Python, PostgreSQL, and Redis on the system and configure the `.env` file.

The `.ps1` scripts are intended for Windows. On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

The dependencies include Windows-specific packages such as `comtypes`; adjust them as necessary for the target operating system.

Configure `REDIS_URL` according to the installed Redis instance.

The requirement for a PostgreSQL schema compatible with the project also applies.

## Verification and Current Status

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py shell -c "from django.core.cache import cache; cache.set('verification', 'ok', 30); print(cache.get('verification')); cache.delete('verification')"
```

Dependencies, Django system checks, and Redis read/write operations have been validated in the local environment.

Running the full dashboard requires a properly configured database with the expected schema.

There are legacy tests and documentation files that still need to be updated to reflect the current state of the application.

One legacy test expects the root route to return `404`, while the root route currently displays the public dashboard.

There is currently no claim that the entire test suite passes successfully.

## Local Files and Deployment

The `.gitignore` excludes:

- Python virtual environments;
- `.env` and local environment variants;
- SQL dumps;
- local databases;
- compressed files;
- private keys;
- logs;
- user uploads in `media/`;
- generated static files in `staticfiles/`;
- Redis executables.

`.env.example` contains sample values and empty fields only.

Interface assets in `static/`, templates, and migrations are included in the repository.

User-uploaded images must be provisioned separately.

For production deployment, configure:

- a unique secret key;
- `DEBUG=False`;
- authorized hosts;
- HTTPS;
- a WSGI/ASGI server;
- PostgreSQL;
- Redis;
- persistent upload storage.

`runserver` is intended for development only.

Before publishing the application, review the static file configuration, SMTP settings, and security configuration.
