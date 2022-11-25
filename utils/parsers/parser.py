import requests
from bs4 import BeautifulSoup
import datetime
from db.models import Event, Fight, Fighter
from db.database import SessionLocal
from datetime import datetime
from db.utils import get_or_create, does_exist

# 1. Идём на http://ufcstats.com/statistics/events/completed, берём предпоследний, переходим на него
# 2. Парсим бои с результатами для прошедшего
# 3. Идём на http://ufcstats.com/statistics/events/completed, берём следующий, преходим на него
# 4. Парсим бои для следующего

# TODO:
# get or create для Бойцов
# get or create для Боёв
# проверка изменений для Ивента


class ParserService:
    URL_EVENTS_LIST = "http://ufcstats.com/statistics/events/completed"

    def parse_next_event(self, url: str) -> None:
        r = requests.get(url)
        assert r.status_code == 200

        page = BeautifulSoup(r.content, "html.parser")

        # get event ref_id
        ref_id = url.split("/")[-1]

        # get event name
        event_name = page.find(class_="b-content__title").get_text(strip=True)

        # get event date
        event_date = (
            page.find(class_="b-list__box-list")
            .find_all("li")[0]
            .get_text(strip=True)
            .split(":")[1]
        )
        event_date_obj = datetime.strptime(event_date, "%B %d, %Y").date()

        # get event location
        event_location = (
            page.find(class_="b-list__box-list")
            .find_all("li")[1]
            .get_text(strip=True)
            .split(":")[1]
        )

        # get fight pairs
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

        db = SessionLocal()
        # save event in db
        event_db = Event(
            name=event_name,
            date=event_date_obj,
            location=event_location,
            url=url,
            ref_id=ref_id,
        )
        db.add(event_db)
        db.commit()

        # save fights
        for fighter1, fighter2 in pairs:
            fighter1_db = Fighter(name=fighter1)
            fighter2_db = Fighter(name=fighter2)
            fight_db = Fight(fighter1=fighter1_db, fighter2=fighter2_db, event=event_db)
            db.add(fighter1_db)
            db.add(fighter2_db)
            db.add(fight_db)
            db.commit()

        print(f"Next Event {event_db.ref_id} | {event_db.name} is created")

    def parse_past_event(self, url: str) -> None:
        r = requests.get(url)
        assert r.status_code == 200

        page = BeautifulSoup(r.content, "html.parser")

        # get event ref_id
        ref_id = url.split("/")[-1]

        # get event name
        event_name = page.find(class_="b-content__title").get_text(strip=True)

        # get event date
        event_date = (
            page.find(class_="b-list__box-list")
            .find_all("li")[0]
            .get_text(strip=True)
            .split(":")[1]
        )
        event_date_obj = datetime.strptime(event_date, "%B %d, %Y").date()

        # get event location
        event_location = (
            page.find(class_="b-list__box-list")
            .find_all("li")[1]
            .get_text(strip=True)
            .split(":")[1]
        )

        # get fight pairs
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

        db = SessionLocal()
        # save event in db
        event_db = Event(
            name=event_name,
            date=event_date_obj,
            location=event_location,
            url=url,
            ref_id=ref_id,
            is_over=True,
        )
        db.add(event_db)
        db.commit()

        # save fights
        for fighter1, fighter2 in pairs:
            fighter1_db = Fighter(name=fighter1)
            fighter2_db = Fighter(name=fighter2)
            fight_db = Fight(
                fighter1=fighter1_db,
                fighter2=fighter2_db,
                winner=fighter1_db,
                event=event_db,
                is_over=True,
            )
            db.add(fighter1_db)
            db.add(fighter2_db)
            db.add(fight_db)
            db.commit()

        print(f"Past Event {event_db.ref_id} | {event_db.name} is created / updated")

    def get_events(self):
        r = requests.get(self.URL_EVENTS_LIST)
        assert r.status_code == 200

        page = BeautifulSoup(r.content, "html.parser")

        table = page.find("tbody")
        # past_event_url = page.find("tbody").find_all(class_="b-statistics__table-row")[1].find("a")["href"]
        past_event_url = table.find_all(class_="b-statistics__table-row")[1].find("a")[
            "href"
        ]

        # next_event_url = page.find("tbody").find_all(class_="b-statistics__table-row_type_first")[0].find("a")["href"]
        next_event_url = table.find_all(class_="b-statistics__table-row_type_first")[
            0
        ].find("a")["href"]

        print("Past", past_event_url)
        print("Next", next_event_url)
        db = SessionLocal()
        past_event_ref_id = past_event_url.split("/")[-1]
        next_event_ref_id = next_event_url.split("/")[-1]
        if not db.query(Event).filter(Event.ref_id == next_event_ref_id).count():
            self.parse_next_event(next_event_url)
        else:
            print("Skip Next")
        if not db.query(Event).filter(Event.ref_id == past_event_ref_id).count():
            self.parse_past_event(past_event_url)
        else:
            print("Skip Past")

    # def update_next_event(self):
    #     pass

    # def get_next_event_fights(self, db: SessionLocal, event: Event) -> str:
    #     r = requests.get(event.url)
    #     assert r.status_code == 200
    #
    #     page = BeautifulSoup(r.content, "html.parser")
    #
    #     pairs = []
    #
    #     trs = page.find_all(
    #         "tr",
    #         class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
    #     )
    #     for tr in trs:
    #         rows = tr.find_all("a", class_="b-link b-link_style_black")[:2]
    #         pair = []
    #         for row in rows:
    #             # print(row.get_text(strip=True))
    #             pair.append(row.get_text(strip=True))
    #         pairs.append(pair)
    #
    #     print(pairs)
    #
    #     # db = SessionLocal()
    #     for fighter1, fighter2 in pairs:
    #         fighter1_db = Fighter(name=fighter1)
    #         fighter2_db = Fighter(name=fighter2)
    #         fight_db = Fight(fighter1=fighter1_db, fighter2=fighter2_db, event=event)
    #         db.add(fighter1_db)
    #         db.add(fighter2_db)
    #         db.add(fight_db)
    #         db.commit()
    #
    #     return "next event is added"
    #
    # def get_next_event(self) -> str:
    #
    #     r = requests.get(self.URL_EVENTS_LIST)
    #     assert r.status_code == 200
    #
    #     r_json = r.json()
    #     next_event_json = r_json[0]
    #     db = SessionLocal()
    #
    #     does_exist = (
    #         db.query(Event).filter(Event.name == next_event_json["event_name"]).count()
    #     )
    #     if does_exist:
    #         return f"Event {next_event_json['event_name']} already exists"
    #
    #     time_json = next_event_json["event_date"].split("T")[0]
    #     time = datetime.strptime(time_json, "%Y-%m-%d")
    #
    #     next_event = Event(
    #         name=next_event_json["event_name"],
    #         date=time,
    #         # date=next_event_json["event_date"],
    #         location=next_event_json["event_location"],
    #         url=next_event_json["event_url"],
    #     )
    #     db.add(next_event)
    #     db.commit()
    #
    #     return self.get_next_event_fights(db, next_event)
    #
    # def parse_all_events(self) -> str:
    #     print("Start to parse")
    #     r = requests.get(self.URL_EVENTS_LIST)
    #     assert r.status_code == 200
    #     r_json = r.json()
    #     db = SessionLocal()
    #     for event_json in r_json:
    #         does_exist = (
    #             db.query(Event).filter(Event.name == event_json["event_name"]).count()
    #         )
    #         print(f"Event {event_json['event_name']} already exists")
    #         if does_exist:
    #             continue
    #
    #         time_json = event_json["event_date"].split("T")[0]
    #         time = datetime.strptime(time_json, "%Y-%m-%d")
    #
    #         event_db = Event(
    #             name=event_json["event_name"],
    #             date=time,
    #             location=event_json["event_location"],
    #             url=event_json["event_url"],
    #             is_over=True if time < datetime.now() else False,
    #         )
    #         db.add(event_db)
    #         db.commit()
    #     return "events are parsed"
    #
    # def parse_fights(self) -> str:
    #     r = requests.get(self.URL_FIGHTS_LIST)
    #     assert r.status_code == 200
    #     r_json = r.json()
    #     db = SessionLocal()
    #     for fight_json in r_json:
    #         # if not does_exists(db, Event, name=fight_json["event"]["event_name"]):
    #         #     continue
    #         fighter1_db = get_or_create(db, Fighter, name=fight_json["fighter1_name"])
    #         fighter2_db = get_or_create(db, Fighter, name=fight_json["fighter2_name"])
    #         winner_db = get_or_create(db, Fighter, name=fight_json["winner"])
    #         event_db = get_or_create(db, Event, name=fight_json["event"]["event_name"])
    #         # event_db = db.query(Event).filter_by(name=fight_json["event"]["event_name"])
    #         fight_db = Fight(
    #             fighter1=fighter1_db,
    #             fighter2=fighter2_db,
    #             winner=winner_db,
    #             is_over=True,
    #             event=event_db,
    #         )
    #         db.add(fight_db)
    #         db.commit()
    #         print(
    #             f"Fight {fight_json['fighter1_name']} vs {fight_json['fighter2_name']} is added"
    #         )
    #     return "fights are parsed"
