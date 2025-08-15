# Ticketing API (Flask)

A clean, modular ticketing API with JWT auth and SQLite (easily swappable).

## Features
- `POST /auth/register` — Register user
- `POST /auth/login` — Obtain JWT
- `POST /tickets` — Create a ticket (JWT required)
- `GET /tickets` — List your tickets with optional filters: `status`, `priority`

### Priorities
- `low`, `medium`, `high`

### Statuses
- `open`, `in_progress`, `closed` (creation defaults to `open`)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
# Visit http://localhost:5000/health
```

### Environment variables (optional)
- `FLASK_ENV` (default: development)
- `DATABASE_URL` (default: sqlite:///ticketing.db)
- `SECRET_KEY` (default: dev-secret-key)
- `JWT_SECRET_KEY` (default: dev-jwt-secret)

## Example usage with curl

```bash
# Register
curl -X POST http://localhost:5000/auth/register -H "Content-Type: application/json"   -d '{"username":"alice","password":"secret123"}'

# Login
curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json"   -d '{"username":"alice","password":"secret123"}'

# Save the token
TOKEN="paste-token-here"

# Create ticket
curl -X POST http://localhost:5000/tickets -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"   -d '{"title":"Cannot login","description":"Login fails with 500","priority":"high"}'

# List tickets (filter by priority)
curl -X GET "http://localhost:5000/tickets?priority=high" -H "Authorization: Bearer $TOKEN"
```

## Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t ticketing-api .
docker run -p 5000:5000 ticketing-api
```

## Project Structure

```
ticketing_api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── ticket_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── ticket_service.py
│   └── utils/
│       ├── __init__.py
│       ├── errors.py
│       └── validators.py
├── tests/
│   ├── test_auth.py
│   └── test_tickets.py
├── run.py
├── requirements.txt
├── Dockerfile
└── README.md
```
