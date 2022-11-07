from db.schemas import FightRead, EventRead
from db.database import SessionLocal
from db.models import Event, Fight, Fighter
import random

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db import models
from db.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"Welcome": "MMA Pet Project"}


@app.get("/read/events", response_model=list[EventRead])
def read_events(db: Session = Depends(get_db)):
    # db = SessionLocal()
    data = db.query(Event).join(Fight).all()
    return data


@app.get("/read/events_simple")
def read_events_simple(db: Session = Depends(get_db)):
    # db = SessionLocal()
    data = db.query(Event).all()
    return data


@app.get("/read/events/{event_id}", response_model=EventRead)
def read_event_by_id(event_id: int, db: Session = Depends(get_db)):
    data = db.query(Event).filter(Event.id == event_id).first()
    return data


@app.get("/read/next_event", response_model=EventRead)
def read_next_event(db: Session = Depends(get_db)):
    data = db.query(Event).order_by(Event.date.desc()).first()
    return data


@app.get("/read/fights", response_model=list[FightRead])
def read_fights(db: Session = Depends(get_db)) -> list[FightRead]:
    data = db.query(Fight).join(Event).all()
    return data


@app.get("/read/fights/{fight_id}", response_model=FightRead)
def read_fights_by_id(fight_id: int, db: Session = Depends(get_db)) -> FightRead:
    data = db.query(Fight).filter(Fight.id == fight_id).join(Event).first()
    return data


@app.get("/read/fighters")
def read_fighters(db: Session = Depends(get_db)) -> dict:
    data = db.query(Fighter).all()
    return data


@app.get("/read/fights2")
def read_fights(db: Session = Depends(get_db)):
    # db = SessionLocal()
    data = db.query(Fight).all()
    return data


@app.get("/create/data")
def generate_data():
    from utils.data_generator import generate_data
    return generate_data()


@app.get("/create/next_event")
def create_next_event():
    from utils.parsers.parser import get_next_event
    return get_next_event()


@app.get("/create/parse_events")
def parse_events():
    from utils.parsers.parser import parse_events
    return parse_events()


@app.get("/create/parse_fights")
def parse_events():
    from utils.parsers.parser import parse_fights
    return parse_fights()


@app.get("/create/init_data")
def init_data():
    from utils.parsers.parser import parse_fights, get_next_event
    print(get_next_event())
    print(parse_fights())
    return "data is initialized"
