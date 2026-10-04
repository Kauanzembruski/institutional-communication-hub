param([string]$Address = '127.0.0.1:8000')
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'institucional.settings'); import django; django.setup(); from django.conf import settings; db=settings.DATABASES['default']; missing=[k for k in ('NAME','USER','PASSWORD') if not db[k]]; import sys; print('Preencha DB_NAME, DB_USER e DB_PASSWORD no .env.') if missing else None; sys.exit(bool(missing))"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& "$PSScriptRoot\start-redis.ps1"
& $python manage.py check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python manage.py runserver $Address
