from pydantic import BaseModel


class BaseSchema(BaseModel):

    class Config:
        orm_mode = True


class EventBase(BaseSchema):
    pass


class FightBase(BaseSchema):
    pass


class FighterBase(BaseSchema):
    pass


class FighterInFight(FighterBase):
    id: int
    name: str
    country: str | None


class FightInEvent(FightBase):
    id: int
    fighter1: FighterInFight
    fighter2: FighterInFight
    winner: FighterInFight | None
    odds_fighter1: float | None
    odds_fighter2: float | None
    is_over: bool | None
    event_id: int | None


class EventRead(EventBase):
    id: int
    name: str
    is_over: bool | None
    date: str | None
    location: str | None
    url: str | None
    fights: list[FightInEvent] = None

###


class EventInFight(EventBase):
    id: int
    name: str
    is_over: bool | None
    date: str | None
    location: str | None
    url: str | None


class FightRead(FightBase):
    id: int
    fighter1: FighterInFight
    fighter2: FighterInFight
    winner: FighterInFight | None
    odds_fighter1: float | None
    odds_fighter2: float | None
    is_over: bool | None
    event_id: int | None
    event: EventInFight



# class EventBase(BaseModel):
#     id: int
#     name: str
#     is_over: bool | None
#     date: str | None
#     location: str | None
#     url: str | None
#
#     class Config:
#         orm_mode = True
#
#
# class FightBase(BaseModel):
#     id: int
#     odds_fighter1: float | None
#     odds_fighter2: float | None
#     is_over: bool | None
#     event_id: int | None
#
#     class Config:
#         orm_mode = True
#
#
# class FighterBase(BaseModel):
#     id: int
#     name: str
#     country: str | None
#
#     class Config:
#         orm_mode = True
#
#
# class EventInFight(EventBase):
#     pass
#
#
# class FightInEvent(FightBase):
#     pass
#
#
# class FighterInFight(FighterBase):
#     pass
#
#
# class FightRead(FightBase):
#     id: int
#     fighter1: FighterInFight
#     fighter2: FighterInFight
#     winner: FighterInFight | None
#     odds_fighter1: float | None
#     odds_fighter2: float | None
#     is_over: bool | None
#     event_id: int | None
#     event: EventInFight
#
#     class Config:
#         orm_mode = True
#
#
# class EventRead(BaseModel):
#     id: int
#     name: str
#     is_over: bool | None
#     date: str | None
#     location: str | None
#     url: str | None
#     fights: list[FightInEvent] = None
#
#     class Config:
#         orm_mode = True
