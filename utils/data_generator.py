from db.database import SessionLocal
from db.models import Event, Fight, Fighter
import random


def generate_data():
    # ADD EVENT
    db = SessionLocal()
    e1 = Event(name=f"test{random.randint(1, 20)}")
    db.add(e1)
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

    # ADD FIGHT
    fight1 = Fight(
        # fighter1=f"fighter{random.randint(1, 20)}",
        # fighter2=f"fighter{random.randint(1, 20)}",
        fighter1_id=fighter1.id,
        fighter2_id=fighter2.id,
        event_id=e1.id,
    )
    fight2 = Fight(
        fighter1_id=fighter2.id,
        fighter2_id=fighter3.id,
        event_id=1
    )
    fight3 = Fight(
        fighter1_id=fighter3.id,
        fighter2_id=fighter1.id,
        event_id=1
    )
    db.add(fight1)
    db.add(fight2)
    db.add(fight3)
    db.commit()
