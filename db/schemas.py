from pydantic import BaseModel


class FightRead(BaseModel):
    id: int
    fighter1: str
    fighter2: str
    odds_fighter1: float | None
    odds_fighter2: float | None
    is_over: bool | None
    event_id: int | None
    # event: EventRead  # TODO

    class Config:
        orm_mode = True


class EventRead(BaseModel):
    id: int
    name: str
    is_over: bool | None
    date: str | None
    location: str | None
    url: str | None
    fights: list[FightRead] = None

    class Config:
        orm_mode = True
