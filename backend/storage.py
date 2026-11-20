"""Storage layer: reads and writes tickets to data/tickets.json.

All file access goes through this module, so the rest of the app
never touches the JSON file directly.
"""
import json
import threading
from pathlib import Path

# backend/storage.py -> project root -> data/tickets.json
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.json"

# Prevents two requests from writing the file at the same time.
_lock = threading.Lock()


def _ensure_file() -> None:
    """Create data/tickets.json with an empty list if it does not exist."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_tickets() -> list[dict]:
    """Return all tickets stored in the JSON file."""
    _ensure_file()
    with _lock:
        text = DATA_FILE.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Corrupted file: treat as empty instead of crashing the API.
        return []
    return data if isinstance(data, list) else []


def save_tickets(tickets: list[dict]) -> None:
    """Overwrite the JSON file with the given list of tickets."""
    _ensure_file()
    with _lock:
        # Write to a temp file first, then replace, so a crash mid-write
        # never leaves a half-written tickets.json.
        tmp = DATA_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(tickets, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(DATA_FILE)


def add_ticket(ticket: dict) -> dict:
    """Assign the next id, append the ticket, save, and return it."""
    tickets = load_tickets()
    next_id = max((t.get("id", 0) for t in tickets), default=0) + 1
    ticket = {"id": next_id, **ticket}
    tickets.append(ticket)
    save_tickets(tickets)
    return ticket
