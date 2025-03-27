"""Database connection and low-level SQL requests."""

import sqlite3
from pathlib import Path
from sqlalchemy import create_engine, func, case, desc
from sqlalchemy.orm import Session

from Model.Class import Country, athlete, discipline, team, event, medal, discipline_athlete

db_url = f"sqlite:///{Path(__file__).parents[1] / 'database' / 'olympics.db'}"
engine = create_engine(db_url)



def get_countries(id=None):
    """Get list of countries.

    If id is not None, the list contains only the country with given id.

    """
    session = Session(engine)
    if id is None:
        rows = session.query(Country).all()
    else:
        rows = session.query(Country).filter(Country.id == id).all()
    return rows


def get_athletes(id=None):
    """Get list of athletes.

    If id is not None, the list contains only the athlete with given id.

    """
    session = Session(engine)
    if id is None:
        rows = session.query(athlete).all()
    else:
        rows = session.query(athlete).filter(athlete.id == id).all()
    return rows


def get_disciplines(id=None):
    """Get list of disciplines.

    If id is not None, the list contains only the discipline with given id.

    """
    session = Session(engine)
    if id is None:
        rows = session.query(discipline).all()
    else:
        rows = session.query(discipline).filter(discipline.id == id).all()
    return rows


def get_teams(id=None):
    """Get list of teams.

    If id is not None, the list contains only the team with given id.

    """
    session = Session(engine)
    if id is None:
        rows = session.query(team).all()
    else:
        rows = session.query(team).filter(team.id == id).all()
    return rows


def get_events(id=None):
    """Get list of events.

    If id is not None, the list contains only the event with given id.

    """
    session = Session(engine)
    if id is None:
        rows = session.query(event).all()
    else:
        rows = session.query(event).filter(event.id == id).all()
    return rows


def get_medals(id=None):
    """Get list of medals.

    If id is not None, the list contains only the medal with given id.

    """
    session = Session(engine)
    if id is None:
        rows = session.query(medal).all()
    else:
        rows = session.query(medal).filter(medal.id == id).all()
    return rows


def get_discipline_athletes(discipline_id):
    """Get athlete ids linked to given discipline id."""
    session = Session(engine)
    rows = session.query(discipline_athlete).filter(discipline_athlete.discipline_id == discipline_id).all()
    return rows


def get_top_countries( top=10):
    """Get medal count ranking of countries."""
    session = Session(engine)
    gold_count = func.sum(case((medal.type == 'gold', 1), else_=0)).label("gold")
    silver_count = func.sum(case((medal.type == 'silver', 1), else_=0)).label("silver")
    bronze_count = func.sum(case((medal.type == 'bronze', 1), else_=0)).label("bronze")

    query = (
        session.query(
            Country.name,
            gold_count,
            silver_count,
            bronze_count
        )
        .outerjoin(team, team.country_id == Country.id)
        .outerjoin(athlete, athlete.country_id == Country.id)
        .outerjoin(medal, (medal.athlete_id == athlete.id) | (medal.team_id == team.id))
        .group_by(Country.id)
        .order_by(desc("gold"), desc("silver"), desc("bronze"))
        .limit(top)
    )

    return query.all()


def get_collective_medals(team_id=None):
    """Get list of medals for team events.

    If team_id is not None, the list contains only the medals won by team with
    given id.

    """
    session = Session(engine)
    query = (
        session.query(
            Country.name,
            discipline.name.label("discipline"),
            event.name.label("event"),
            medal.type,
            medal.date
        )
        .join(team, medal.team_id == team.id)
        .join(Country, team.country_id == Country.id)
        .join(event, medal.event_id == event.id)
        .join(discipline, event.discipline_id == discipline.id)
    )

    if team_id is not None:
        query = query.filter(team.id == team_id)

    rows = query.all()
    session.close()
    return rows


def get_top_collective(top=10):
    """Get medal count ranking of countries for team events.

    Number of countries is limited to the given top number.

    """
    session = Session(engine)
    query = (
        session.query(
            Country.name.label("country"),
            func.count(medal.id).label("medals")
        )
        .join(team, medal.team_id == team.id)
        .join(Country, team.country_id == Country.id)
        .group_by(Country.name)
        .order_by(desc("medals"))
        .limit(top)
    )
    rows = query.all()
    session.close()
    return rows


def get_individual_medals(athlete_id=None):
    """Get list of medals for individual events.

    If athlete_id is not None, the list contains only the medals won by athlete
    with given id.

    """
    session = Session(engine)
    query = (
        session.query(
            athlete.name,
            Country.name.label("country"),
            discipline.name.label("discipline"),
            event.name.label("event"),
            medal.type,
            medal.date
        )
        .join(Country, athlete.country_id == Country.id)
        .join(event, medal.event_id == event.id)
        .join(discipline, event.discipline_id == discipline.id)
    )
    if athlete_id is not None:
        query = query.filter(athlete.id == athlete_id)
    rows = query.all()
    session.close()
    return rows


def get_top_individual(top=10):
    """Get medal count ranking of athletes for individual events.

    Number of athletes is limited to the given top number.

    """
    session = Session(engine)
    query = (
        session.query(
            athlete.name,
            athlete.gender,
            Country.name.label("country"),
            func.count(medal.id).label("medals")
        )
        .join(medal, medal.athlete_id == athlete.id)
        .join(Country, athlete.country_id == Country.id)
        .group_by(athlete.name, athlete.gender, Country.name)
        .order_by(desc("medals"))
        .limit(top)
    )
    rows = query.all()
    session.close()
    return rows
