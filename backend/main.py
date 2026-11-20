"""NU Campus Helpdesk - FastAPI backend.

Run from the project root:
    uvicorn backend.main:app --reload
Then open http://127.0.0.1:8000/docs
"""
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:  # works with `uvicorn backend.main:app`
    from backend import storage
except ImportError:  # works with `cd backend && uvicorn main:app`
    import storage

app = FastAPI(title="NU Campus Helpdesk API", version="1.0.0")

# Allow the frontend (opened from any local origin) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TicketCreate(BaseModel):
    """What the client sends to create a ticket."""
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    category: str = Field("General", max_length=50)
    student_name: str = Field(..., min_length=1, max_length=100)


class Ticket(TicketCreate):
    """What the API returns: the input plus server-generated fields."""
    id: int
    status: str
    created_at: str


@app.get("/")
def root():
    return {"message": "NU Campus Helpdesk API is running. See /docs"}


@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(ticket: TicketCreate):
    new_ticket = {
        **ticket.model_dump(),
        "status": "Open",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    return storage.add_ticket(new_ticket)


@app.get("/tickets", response_model=list[Ticket])
def list_tickets():
    return storage.load_tickets()
