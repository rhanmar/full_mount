import pytest
# from .factories import fighter_factory
from fastapi import status
from db.models import Event, Fight, Fighter


def test_fighters_list(test_db, client, db_session, fighter_factory):
    fighters = [fighter_factory() for _ in range(20)]
    db_session.commit()
    assert db_session.query(Fighter).count() == len(fighters)
    response = client.get("read/fighters")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(fighters)


def test_events_list(test_db, client, db_session, fighter_factory, event_factory, fight_factory):
    fighters = [fighter_factory() for _ in range(20)]
    events = [event_factory() for _ in range(2)]
    fights1 = [fight_factory(fighter1=fighters[0], fighter2=fighters[1], event=events[0]) for _ in range(4)]
    fights2 = [fight_factory(fighter1=fighters[2], fighter2=fighters[3], event=events[1]) for _ in range(4)]
    db_session.commit()
    assert db_session.query(Fighter).count() == len(fighters)
    response = client.get("read/events")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(events)
