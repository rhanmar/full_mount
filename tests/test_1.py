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
    # assert response.json() == {'asd'}
    assert len(response.json()) == len(fighters)


