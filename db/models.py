from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from db.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    ref_id = Column(String, unique=True, index=True)
    ref_url = Column(String, nullable=True)
    name = Column(String)
    is_over = Column(Boolean, default=False)
    date = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    fights = relationship("Fight", back_populates="event")


class Fighter(Base):
    __tablename__ = "fighters"

    id = Column(Integer, primary_key=True, index=True)
    ref_id = Column(String, unique=True, index=True)
    ref_url = Column(String, nullable=True)
    name = Column(String)
    country = Column(String, nullable=True)
    # fights = relationship("Fight")
    # fights = relationship("Fight")


class Fight(Base):
    __tablename__ = "fights"

    id = Column(Integer, primary_key=True, index=True)
    ref_id = Column(String, unique=True, index=True)
    ref_url = Column(String, nullable=True)

    fighter1_id = Column(Integer, ForeignKey("fighters.id"))
    fighter1 = relationship("Fighter", foreign_keys=[fighter1_id])

    fighter2_id = Column(Integer, ForeignKey("fighters.id"))
    fighter2 = relationship("Fighter", foreign_keys=[fighter2_id])

    winner_id = Column(Integer, ForeignKey("fighters.id"), nullable=True)
    winner = relationship("Fighter", foreign_keys=[winner_id])

    odds_fighter1 = Column(Float, nullable=True)
    odds_fighter2 = Column(Float, nullable=True)
    is_over = Column(Boolean, default=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="fights")
