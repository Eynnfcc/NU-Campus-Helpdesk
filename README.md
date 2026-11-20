# NU Campus Helpdesk

A simple helpdesk where students submit support tickets. The backend is a
FastAPI app that stores tickets in a JSON file.

## Project structure

```
backend/
  main.py           # API routes (POST /tickets, GET /tickets)
  storage.py        # reads/writes data/tickets.json
  requirements.txt  # Python dependencies
data/
  tickets.json      # the "database" (starts as [])
```

## Run the API

From the project root:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Then open http://127.0.0.1:8000/docs. It's an interactive page where you can
try every endpoint.

## Endpoints

| Method | Path       | What it does              |
|--------|------------|---------------------------|
| GET    | `/`        | Health check              |
| POST   | `/tickets` | Create a ticket (201)     |
| GET    | `/tickets` | List all tickets          |

### Create a ticket – request body

```json
{
  "title": "WiFi not working",
  "description": "No WiFi in Building B since morning",
  "category": "IT",
  "student_name": "Ahmed"
}
```

`category` is optional (default `"General"`). The server adds `id`,
`status` (`"Open"`), and `created_at`.

### Example with curl

```bash
curl -X POST http://127.0.0.1:8000/tickets -H "Content-Type: application/json" -d "{\"title\":\"WiFi\",\"description\":\"No WiFi\",\"student_name\":\"Ahmed\"}"
```

```bash
curl http://127.0.0.1:8000/tickets
```

## Team

- **Eyad** – Team Leader, Backend (API, storage, integration)
- **Aya** – (fill in role)
- **Yassin** – (fill in role)
