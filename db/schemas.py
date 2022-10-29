from pydantic import BaseModel


class EventBase(BaseModel):
    id: int
    name: str
    is_over: bool | None
    date: str | None
    location: str | None
    url: str | None

    class Config:
        orm_mode = True


class FightBase(BaseModel):
    id: int
    fighter1: str
    fighter2: str
    odds_fighter1: float | None
    odds_fighter2: float | None
    is_over: bool | None
    event_id: int | None

    class Config:
        orm_mode = True


class EventInFight(EventBase):
    pass


class FightInEvent(FightBase):
    pass


class FightRead(BaseModel):
    id: int
    fighter1: str
    fighter2: str
    odds_fighter1: float | None
    odds_fighter2: float | None
    is_over: bool | None
    event_id: int | None
    event: EventInFight

    class Config:
        orm_mode = True


class EventRead(BaseModel):
    id: int
    name: str
    is_over: bool | None
    date: str | None
    location: str | None
    url: str | None
    fights: list[FightInEvent] = None

    class Config:
        orm_mode = True
