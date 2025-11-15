# SmartLib DB Project

## Requirements
- Docker / Docker Compose
- Python
- Git

## Launching a web application
...

## Database development

### Preparing the environment

1. Create a DB user:
```bash
cp db/init/01-user.sql.template db/init/01-user.sql
```

Edit `db/init/01-user.sql`, replacing:
- `{{USERNAME}}` with your username (this can be your name)
- `{{PASSWORD}}` with your password

2. Copy the config template:
```bash
cp .env.example .env # CHANGE THE VALUES TO YOUR OWN
cp docker-compose.override.yml.example docker-compose.override.yml # you need to know the password!!!
```

3. Run the container:
```bash
docker compose up -d
```

4. Install Python dependencies:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

5. Apply migrations:
```bash
alembic upgrade head
```

7. Connect to the database:
```bash
psql -h 127.0.0.1 -p 5433 -U {{USERNAME}} -d smartlib
```

## Project structure
```
DB_project/
├─ alembic/              # migrations
├─ app/
│  └─ models.py          # ORM-models
├─ db/init/              # init-scripts for Docker
├─ docker-compose.yml
├─ .env.example
├─ requirements.txt
└─ README.md
```