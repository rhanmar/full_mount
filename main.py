from db.schemas import FightRead, EventRead
from db.database import SessionLocal
from db.models import Event, Fight, Fighter
import random

from fastapi import FastAPI

from db import models
from db.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root() -> dict:
    return {"Welcome": "MMA Pet Project"}


@app.get("/create/event")
def create_event():
    db = SessionLocal()
    e1 = Event(name=f"test{random.randint(1, 20)}")
    db.add(e1)
    db.commit()
    return {"ok": e1.id}


@app.get("/read/events", response_model=list[EventRead])
def read_events():
    db = SessionLocal()
    data = db.query(Event).join(Fight).all()
    return data


@app.get("/read/events_simple")
def read_events_simple():
    db = SessionLocal()
    data = db.query(Event).all()
    return data


@app.get("/read/events/{event_id}", response_model=EventRead)
def read_event_by_id(event_id: int):
    db = SessionLocal()
    data = db.query(Event).filter(Event.id == event_id).first()
    return data


@app.get("/create/fight")
def create_fight():
    db = SessionLocal()
    f1 = Fight(
        fighter1=f"fighter{random.randint(1, 20)}",
        fighter2=f"fighter{random.randint(1, 20)}",
        event_id=1
    )
    db.add(f1)
    db.commit()
    return {"ok": f1.id}


@app.get("/read/fights", response_model=list[FightRead])
def read_fights() -> list[FightRead]:
    db = SessionLocal()
    data = db.query(Fight).join(Event).all()
    return data


@app.get("/read/fights/{fight_id}", response_model=FightRead)
def read_fights_by_id(fight_id: int) -> FightRead:
    db = SessionLocal()
    data = db.query(Fight).filter(Fight.id == fight_id).join(Event).first()
    return data


@app.get("/read/fighters")
def read_fighters() -> dict:
    db = SessionLocal()
    data = db.query(Fighter).all()
    return data


@app.get("/create/fighter")
def create_fighter():
    db = SessionLocal()
    f1 = Fighter(
        name=f"Fighter{random.randint(1, 20)}",
        country="t",
    )
    db.add(f1)
    db.commit()
    return {"ok": f1.id}


@app.get("/read/fights2")
def read_fights():
    db = SessionLocal()
    data = db.query(Fight).all()
    return data


@app.get("/create/data")
def generate_data():
    from utils.data_generator import generate_data
    generate_data()
    return "ok"


@app.get("/create/next_event")
def generate_data():
    from utils.parsers.parser import get_next_event
    get_next_event()
    return "next event is added"
