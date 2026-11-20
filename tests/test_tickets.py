"""Tests for the tickets API (POST /tickets and GET /tickets) and storage."""
from backend import storage


# ---------- Health check ----------

def test_root_returns_running_message(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"]


# ---------- GET /tickets ----------

def test_list_tickets_empty_at_start(client):
    response = client.get("/tickets")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tickets_returns_created_tickets(client, sample_ticket):
    client.post("/tickets", json=sample_ticket)
    client.post("/tickets", json={**sample_ticket, "title": "Projector broken"})

    tickets = client.get("/tickets").json()
    assert len(tickets) == 2
    assert [t["title"] for t in tickets] == ["WiFi not working", "Projector broken"]


# ---------- POST /tickets ----------

def test_create_ticket_returns_201_and_ticket(client, sample_ticket):
    response = client.post("/tickets", json=sample_ticket)
    assert response.status_code == 201

    ticket = response.json()
    assert ticket["id"] == 1
    assert ticket["status"] == "Open"
    assert ticket["created_at"]
    for field, value in sample_ticket.items():
        assert ticket[field] == value


def test_create_ticket_ids_increase(client, sample_ticket):
    first = client.post("/tickets", json=sample_ticket).json()
    second = client.post("/tickets", json=sample_ticket).json()
    assert (first["id"], second["id"]) == (1, 2)


def test_create_ticket_default_category(client, sample_ticket):
    del sample_ticket["category"]
    response = client.post("/tickets", json=sample_ticket)
    assert response.status_code == 201
    assert response.json()["category"] == "General"


def test_create_ticket_missing_field_returns_422(client, sample_ticket):
    del sample_ticket["title"]
    response = client.post("/tickets", json=sample_ticket)
    assert response.status_code == 422


def test_create_ticket_empty_field_returns_422(client, sample_ticket):
    sample_ticket["student_name"] = ""
    response = client.post("/tickets", json=sample_ticket)
    assert response.status_code == 422


def test_client_cannot_set_status_or_id(client, sample_ticket):
    response = client.post(
        "/tickets", json={**sample_ticket, "id": 99, "status": "Resolved"}
    )
    ticket = response.json()
    assert ticket["id"] == 1
    assert ticket["status"] == "Open"


# ---------- Storage (tickets.json) ----------

def test_ticket_is_saved_to_json_file(client, sample_ticket):
    client.post("/tickets", json=sample_ticket)
    saved = storage.load_tickets()
    assert len(saved) == 1
    assert saved[0]["title"] == sample_ticket["title"]
    assert storage.DATA_FILE.exists()


def test_missing_file_is_created_as_empty_list(client):
    assert not storage.DATA_FILE.exists()
    assert storage.load_tickets() == []
    assert storage.DATA_FILE.read_text(encoding="utf-8") == "[]"


def test_corrupted_file_returns_empty_list(client):
    storage.DATA_FILE.write_text("{ not valid json", encoding="utf-8")
    assert storage.load_tickets() == []
