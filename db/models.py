from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, Float
from sqlalchemy.orm import relationship

from db.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_over = Column(Boolean, default=False)
    date = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    url = Column(String, nullable=True)
    # fights = relationship("Fight", back_populates="event")

#
# class Fight(Base):
#     __tablename__ = "fights"
#
#     fighter1_id = Column(Integer, ForeignKey("fighter1.id"))
#     # fighter1 = relationship("Fighter", back_populates="fights")
#     fighter2_id = Column(Integer, ForeignKey("fighter2.id"))
#     # fighter2 = relationship("Fighter", back_populates="fights")
#     winner_id = Column(Integer, ForeignKey("winner.id"), nullable=True)
#     # winner = relationship("Fighter", back_populates="fights")
#     odds_fighter1 = Column(Float, nullable=True)
#     odds_fighter2 = Column(Float, nullable=True)
#     is_over = Column(Boolean, default=False)
#     event_id = Column(Integer, ForeignKey("event.id"))
#     event = relationship("Event", back_populates="fights")
#
#
# class Fighter(Base):
#     __tablename__ = "fighters"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     country = Column(String, nullable=True)
#     fights = relationship("Fight", back_populates="fighter")
