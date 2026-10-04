# Mural Institucional IFRS

Aplicação web para centralizar a comunicação institucional: avisos, eventos, lembretes, cardápio, provas, próximas aulas, datas importantes e achados e perdidos. Reúne um painel público para consulta e exibição em telas, uma área autenticada de gestão e o Django Admin.

## Stack

| Camada | Tecnologias |
| --- | --- |
| Linguagem | Python; ambiente local validado com Python 3.14 |
| Backend | Django 6.0.3, views, templates e ORM |
| Banco | PostgreSQL e psycopg2-binary |
| Cache | Redis e django-redis 7.0.0 |
| Controle de requisições | django-ratelimit 4.1.0 com Redis |
| Interface | HTML, CSS e JavaScript com Django Templates |
| Configuração | python-decouple e variáveis em `.env` |
| Arquivos estáticos | Django Staticfiles e middleware WhiteNoise |
| Integração externa | Open-Meteo, consultada com Requests para informações de clima |
| Autenticação | Sessões, autenticação e recuperação de senha do Django |
| Entrada de servidor | WSGI e ASGI; Gunicorn nas dependências para Linux |

As versões estão em [`requirements.txt`](requirements.txt). O desenvolvimento local usa Redis diretamente no Windows, sem Docker. As bibliotecas adicionais presentes nas dependências não representam necessariamente funcionalidades ativas.

## Funcionalidades

- Painel público com informações institucionais e clima.
- Área autenticada para manutenção de conteúdo e Django Admin.
- Avisos institucionais, lembretes e informações operacionais.
- Agenda de eventos e datas importantes.
- Cardápio e calendário de provas.
- Consulta de próximas aulas por curso/turma.
- Cadastro de achados e perdidos com imagens.
- Recuperação de senha por email.
- Limitação de requisições em operações como login, uploads e exclusões.

## Organização

```text
IFATUALIZADO/
├── institucional/       # Configurações, URLs, WSGI e ASGI
├── apps/
│   ├── core/            # Recursos compartilhados e controle de requisições
│   └── dashboard/       # Modelos e views do mural e da gestão
├── achadoseperdidos/    # Itens encontrados
├── avisosinst/          # Avisos institucionais
├── cardapio/            # Cardápio
├── datasimport/         # Datas importantes
├── eventos/            # Eventos
├── infop/               # Informações operacionais
├── lembretes/           # Lembretes
├── provas/              # Calendário de provas
├── pxaulas/             # Próximas aulas
├── templates/           # Páginas e templates de email
├── static/              # CSS, JavaScript e imagens da interface
├── docs/                # Documentação e referências históricas
├── .env.example         # Configuração sem credenciais
├── manage.py
├── requirements.txt
├── start-redis.ps1      # Inicialização do Redis no Windows
└── runserver.ps1        # Inicialização do ambiente local
```

## Pré-requisitos

- Git e Python 3.12 ou superior, compatível com Django 6. Os comandos abaixo usam Python 3.14, validado localmente.
- PostgreSQL acessível com um esquema compatível com os modelos do projeto.
- Redis. A configuração local usa `127.0.0.1:6380`, banco Redis `1`.
- PowerShell para os scripts de inicialização no Windows.

## Instalação no Windows

### 1. Clonar e criar a venv

```powershell
git clone https://github.com/Kauanzembruski/IFATUALIZADO.git
cd IFATUALIZADO
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

A ativação é opcional quando os comandos usam o caminho completo do Python. Para ativar: `.\.venv\Scripts\Activate.ps1`.

### 2. Configurar o ambiente

```powershell
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copie a chave gerada para `SECRET_KEY` e preencha as credenciais no `.env`.

| Variável | Finalidade | Valor local |
| --- | --- | --- |
| `DEBUG` | Desenvolvimento | `True` |
| `SECRET_KEY` | Chave do Django | Gere uma chave própria |
| `ALLOWED_HOSTS` | Hosts separados por vírgula | `localhost,127.0.0.1` |
| `DB_NAME` | Nome do banco PostgreSQL | Preencher |
| `DB_USER` | Usuário do banco | Preencher |
| `DB_PASSWORD` | Senha do banco | Preencher |
| `DB_HOST` | Endereço do PostgreSQL | `localhost` |
| `DB_PORT` | Porta do PostgreSQL | `5432` |
| `REDIS_URL` | Conexão para cache | `redis://127.0.0.1:6380/1` |
| `EMAIL_BACKEND` | Backend de email | Console no desenvolvimento |

Para SMTP, configure também `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` e, se necessário, `DEFAULT_FROM_EMAIL` e `SERVER_EMAIL`. Com o backend de console, as mensagens de recuperação aparecem no terminal.

### 3. Instalar Redis sem Docker

O script usa a distribuição comunitária [Redis 8.10.2 para Windows x64 Cygwin](https://github.com/redis-windows/redis-windows/releases/tag/8.10.2). Baixe e extraia:

```powershell
New-Item -ItemType Directory -Path tools\redis -Force
Invoke-WebRequest 'https://github.com/redis-windows/redis-windows/releases/download/8.10.2/Redis-8.10.2-Windows-x64-cygwin.zip' -OutFile tools\redis.zip
Expand-Archive tools\redis.zip -DestinationPath tools\redis -Force
```

A pasta resultante deve ser `tools\redis\Redis-8.10.2-Windows-x64-cygwin`. Crie nela o arquivo `redis-local.conf` com:

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

Inicie e verifique:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-redis.ps1
& .\tools\redis\Redis-8.10.2-Windows-x64-cygwin\redis-cli.exe -p 6380 ping
```

O retorno esperado é `PONG`. Redis fica em segundo plano, restrito à máquina local, como cache sem persistência. A porta 6380 evita conflitos com serviços em 6379. Os executáveis não são versionados. Para encerrar:

```powershell
& .\tools\redis\Redis-8.10.2-Windows-x64-cygwin\redis-cli.exe -p 6380 shutdown
```

### 4. Preparar o PostgreSQL

O projeto combina modelos gerenciados pelo Django com modelos `managed = False`, associados a tabelas existentes. Portanto, **`migrate` não cria todas as tabelas de negócio**.

Disponibilize um esquema PostgreSQL compatível com os modelos atuais antes de usar o painel. Se tiver um backup autorizado, restaure-o separadamente. Dumps e dados reais não são publicados.

`docs/criar_banco_postgresql.txt` é uma referência histórica, não um instalador completo do esquema atual. Contém comandos de exclusão e recriação de banco e tabelas; revise antes de usar e não execute sobre dados que deseja preservar.

Com o esquema correto e as credenciais preenchidas:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py check
```

### 5. Executar

```powershell
powershell -ExecutionPolicy Bypass -File .\runserver.ps1
```

O script verifica o preenchimento das credenciais, inicia o Redis, executa as verificações do Django e inicia o servidor em `http://127.0.0.1:8000`.

| Rota | Área |
| --- | --- |
| `/` | Painel público |
| `/home/` | Entrada da área autenticada |
| `/home/painel/` | Painel de gestão |
| `/admin/` | Django Admin |
| `/home/esqueci-senha/` | Recuperação de senha |
| `/lembretePublico/` | Tela pública de lembretes |

Para outra porta: `powershell -ExecutionPolicy Bypass -File .\runserver.ps1 -Address 127.0.0.1:8001`.

## Linux e macOS

Instale Python, PostgreSQL e Redis no sistema e configure o `.env`. Os scripts `.ps1` são voltados ao Windows; em outros sistemas:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

As dependências incluem pacotes específicos do Windows, como `comtypes`; ajuste-os para o sistema de destino quando necessário. Configure `REDIS_URL` conforme o Redis instalado. A exigência de um esquema PostgreSQL compatível também se aplica.

## Verificação e estado atual

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py shell -c "from django.core.cache import cache; cache.set('verificacao', 'ok', 30); print(cache.get('verificacao')); cache.delete('verificacao')"
```

As dependências, as verificações do Django e a escrita/leitura do Redis foram validadas no ambiente local. A execução completa do painel depende do banco configurado e do esquema adequado.

Há testes e documentação legados que precisam de revisão para corresponder ao painel atual. Um teste antigo espera 404 na rota raiz, que atualmente exibe o painel público. Não há declaração de que a suíte completa passe.

## Arquivos locais e publicação

O `.gitignore` exclui ambientes Python, `.env` e variantes locais, dumps SQL, bancos locais, arquivos compactados, chaves privadas, logs, uploads em `media/`, estáticos gerados em `staticfiles/` e executáveis do Redis. `.env.example` contém exemplos e campos vazios.

Os assets de interface em `static/`, templates e migrações fazem parte do código. Imagens enviadas por usuários precisam ser provisionadas separadamente.

Para produção, configure uma chave própria, `DEBUG=False`, hosts autorizados, HTTPS, servidor WSGI/ASGI, PostgreSQL, Redis e armazenamento de uploads. `runserver` serve ao desenvolvimento. Revise arquivos estáticos, SMTP e configurações de segurança antes de disponibilizar o sistema.
