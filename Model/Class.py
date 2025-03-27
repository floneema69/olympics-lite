from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass
class Country(Base):
    __tablename__ = 'country'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False,unique=True)
    name: Mapped[str] = mapped_column(nullable=False)

class athlete(Base):
    __tablename__ = 'athlete'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    __table_args__ = (
        CheckConstraint(gender.in_(['female', 'male'])),
    )

class discipline(Base):
    __tablename__ = 'discipline'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

class team(Base):
    __tablename__ = 'team'
    id: Mapped[int] = mapped_column(primary_key=True)
    gender: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    discipline_id: Mapped[int] = mapped_column(ForeignKey('discipline.id'))
    __table_args__ = (
        CheckConstraint(gender.in_(['female', 'male','mixed'])),
    )

class discipline_athlete(Base):
    __tablename__ = 'discipline_athlete'
    discipline_id: Mapped[int] = mapped_column(ForeignKey('discipline.id'), primary_key=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey('athlete.id'), primary_key=True)

class event(Base):
    __tablename__ = 'event'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    discipline_id: Mapped[int] = mapped_column(ForeignKey('discipline.id'))
    gender: Mapped[str] = mapped_column(nullable=False)
    __table_args__ = (
        CheckConstraint(gender.in_(['female', 'male','mixed'])),
    )
class medal(Base):
    __tablename__ = 'medal'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    athlete_id: Mapped[int] = mapped_column(ForeignKey('athlete.id'))
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id'))
    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    __table_args__ = (
        CheckConstraint(type.in_(['gold', 'silver','bronze'])),
    )