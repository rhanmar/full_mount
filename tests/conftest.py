from db.models import Event, Fight, Fighter
import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def fighter_factory(db_session):
    class FighterFactory(factory.alchemy.SQLAlchemyModelFactory):

        name = factory.Faker("name")

        class Meta:
            model = Fighter
            sqlalchemy_session = db_session
    return FighterFactory


@pytest.fixture()
def event_factory(db_session):
    class EventFactory(factory.alchemy.SQLAlchemyModelFactory):

        name = factory.Faker("name")
        date = factory.Faker("date_object")
        location = factory.Faker("city")
        url = factory.Faker("url")

        class Meta:
            model = Event
            sqlalchemy_session = db_session
    return EventFactory


@pytest.fixture()
def fight_factory(db_session, fighter_factory, event_factory):
    class FightFactory(factory.alchemy.SQLAlchemyModelFactory):

        fighter1 = factory.SubFactory(fighter_factory)
        fighter2 = factory.SubFactory(fighter_factory)
        event = factory.SubFactory(event_factory)

        class Meta:
            model = Fight
            sqlalchemy_session = db_session
    return FightFactory
