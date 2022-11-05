from db.database import SessionLocal
from db.models import Event, Fight, Fighter
import random
import datetime


def generate_data() -> str | None:
    # ADD EVENTS
    db = SessionLocal()
    now = datetime.datetime.now()
    e1 = Event(
        name=f"Event {random.randint(1, 20)}",
        date=now - datetime.timedelta(days=2),
    )
    db.add(e1)
    e2 = Event(
        name=f"Event {random.randint(1, 20)}",
        date=now - datetime.timedelta(days=3)
    )
    db.add(e2)
    db.commit()

    # ADD FIGHTERS
    fighter1 = Fighter(
        name=f"Fighter name {random.randint(1, 20)}",
        country="ru",
    )
    fighter2 = Fighter(
        name=f"Fighter name{random.randint(1, 20)}",
        country="usa",
    )
    fighter3 = Fighter(
        name=f"Fighter name {random.randint(1, 20)}",
        country="br",
    )
    db.add(fighter1)
    db.add(fighter2)
    db.add(fighter3)
    db.commit()

    # ADD FIGHTS
    fight1 = Fight(
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        winner_id=fighter2.id,
        event_id=e1.id,
        is_over=True,
    )
    fight2 = Fight(
        fighter1_id=fighter2.id,
        fighter2_id=fighter3.id,
        event_id=e2.id,
    )
    fight3 = Fight(
        fighter1_id=fighter3.id,
        fighter2_id=fighter1.id,
        event_id=e1.id,
    )
    db.add(fight1)
    db.add(fight2)
    db.add(fight3)
    db.commit()

    return "ok"
