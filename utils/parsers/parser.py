import requests
from bs4 import BeautifulSoup
from db.models import Event, Fight, Fighter
from db.database import SessionLocal
from datetime import datetime
from db.utils import get_or_create, does_exists


class ParserService:
    URL_FIGHTS_LIST = (
        "http://www.ufcstatsapi.com/fights/?skip=0&limit=20&date_descending=true"
    )
    URL_EVENTS_LIST = (
        "http://www.ufcstatsapi.com/events/?skip=0&limit=3&date_descending=true"
    )

    def get_next_event_fights(self, db: SessionLocal, event: Event) -> str:
        r = requests.get(event.url)
        assert r.status_code == 200

        page = BeautifulSoup(r.content, "html.parser")

        pairs = []

        trs = page.find_all(
            "tr",
            class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
        )
        for tr in trs:
            rows = tr.find_all("a", class_="b-link b-link_style_black")[:2]
            pair = []
            for row in rows:
                # print(row.get_text(strip=True))
                pair.append(row.get_text(strip=True))
            pairs.append(pair)

        print(pairs)

        # db = SessionLocal()
        for fighter1, fighter2 in pairs:
            fighter1_db = Fighter(name=fighter1)
            fighter2_db = Fighter(name=fighter2)
            fight_db = Fight(fighter1=fighter1_db, fighter2=fighter2_db, event=event)
            db.add(fighter1_db)
            db.add(fighter2_db)
            db.add(fight_db)
            db.commit()

        return "next event is added"

    def get_next_event(self) -> str:

        r = requests.get(self.URL_EVENTS_LIST)
        assert r.status_code == 200

        r_json = r.json()
        next_event_json = r_json[0]
        db = SessionLocal()

        does_exist = (
            db.query(Event).filter(Event.name == next_event_json["event_name"]).count()
        )
        if does_exist:
            return f"Event {next_event_json['event_name']} already exists"

        time_json = next_event_json["event_date"].split("T")[0]
        time = datetime.strptime(time_json, "%Y-%m-%d")

        next_event = Event(
            name=next_event_json["event_name"],
            date=time,
            # date=next_event_json["event_date"],
            location=next_event_json["event_location"],
            url=next_event_json["event_url"],
        )
        db.add(next_event)
        db.commit()

        return self.get_next_event_fights(db, next_event)

    def parse_all_events(self) -> str:
        print("Start to parse")
        r = requests.get(self.URL_EVENTS_LIST)
        assert r.status_code == 200
        r_json = r.json()
        db = SessionLocal()
        for event_json in r_json:
            does_exist = (
                db.query(Event).filter(Event.name == event_json["event_name"]).count()
            )
            print(f"Event {event_json['event_name']} already exists")
            if does_exist:
                continue

            time_json = event_json["event_date"].split("T")[0]
            time = datetime.strptime(time_json, "%Y-%m-%d")

            event_db = Event(
                name=event_json["event_name"],
                date=time,
                location=event_json["event_location"],
                url=event_json["event_url"],
                is_over=True if time < datetime.now() else False,
            )
            db.add(event_db)
            db.commit()
        return "events are parsed"

    def parse_fights(self) -> str:
        r = requests.get(self.URL_FIGHTS_LIST)
        assert r.status_code == 200
        r_json = r.json()
        db = SessionLocal()
        for fight_json in r_json:
            # if not does_exists(db, Event, name=fight_json["event"]["event_name"]):
            #     continue
            fighter1_db = get_or_create(db, Fighter, name=fight_json["fighter1_name"])
            fighter2_db = get_or_create(db, Fighter, name=fight_json["fighter2_name"])
            winner_db = get_or_create(db, Fighter, name=fight_json["winner"])
            event_db = get_or_create(db, Event, name=fight_json["event"]["event_name"])
            # event_db = db.query(Event).filter_by(name=fight_json["event"]["event_name"])
            fight_db = Fight(
                fighter1=fighter1_db,
                fighter2=fighter2_db,
                winner=winner_db,
                is_over=True,
                event=event_db,
            )
            db.add(fight_db)
            db.commit()
            print(
                f"Fight {fight_json['fighter1_name']} vs {fight_json['fighter2_name']} is added"
            )
        return "fights are parsed"
