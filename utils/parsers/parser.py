import requests
from bs4 import BeautifulSoup
import datetime
from db.models import Event, Fight, Fighter
from db.database import SessionLocal
from datetime import datetime
from db.utils import get_or_create, check_does_exist, get_ref_id_from_url

# 1. Идём на http://ufcstats.com/statistics/events/completed, берём предпоследний, переходим на него
# 2. Парсим бои с результатами для прошедшего
# 3. Идём на http://ufcstats.com/statistics/events/completed, берём следующий, преходим на него
# 4. Парсим бои для следующего


class ParserService:
    URL_EVENTS_LIST = "http://ufcstats.com/statistics/events/completed"

    @staticmethod
    def parse_next_event(url: str) -> None:
        r = requests.get(url)
        assert r.status_code == 200

        page = BeautifulSoup(r.content, "html.parser")

        # get event ref_id
        event_ref_id = get_ref_id_from_url(url)

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

        # get fight data (ref_id, pairs)
        fight_data: dict[str, list[tuple[str, str]]] = {}
        trs = page.find_all(
            "tr",
            class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
        )
        for tr in trs:
            fight_ref_url = tr.find_all("a")[2]["data-link"]
            rows = tr.find_all("a", class_="b-link b-link_style_black")[:2]
            pair = []
            for row in rows:
                fighter_ref_url = row["href"]
                fighter_name = row.get_text(strip=True)
                fighter_data: tuple[str, str] = (fighter_ref_url, fighter_name)
                pair.append(fighter_data)
            fight_data[fight_ref_url] = pair

        db = SessionLocal()

        # save event in db
        event_db = Event(
            name=event_name,
            date=event_date_obj,
            location=event_location,
            ref_url=url,
            ref_id=event_ref_id,
        )
        db.add(event_db)
        db.commit()

        # save fights in db
        for fight_ref_url, pair in fight_data.items():
            fight_ref_id = get_ref_id_from_url(fight_ref_url)
            fighter1_ref_url, fighter1_name = pair[0]
            fighter2_ref_url, fighter2_name = pair[1]
            fighter1_ref_id = get_ref_id_from_url(fighter1_ref_url)
            fighter2_ref_id = get_ref_id_from_url(fighter2_ref_url)
            fighter1_db = get_or_create(
                db,
                Fighter,
                ref_id=fighter1_ref_id,
                ref_url=fighter1_ref_url,
                name=fighter1_name,
            )
            fighter2_db = get_or_create(
                db,
                Fighter,
                ref_id=fighter2_ref_id,
                ref_url=fighter2_ref_url,
                name=fighter2_name,
            )
            fight_db = get_or_create(
                db,
                Fight,
                ref_id=fight_ref_id,
                ref_url=fight_ref_url,
                fighter1=fighter1_db,
                fighter2=fighter2_db,
                event=event_db,
            )
            db.add(fighter1_db)
            db.add(fighter2_db)
            db.add(fight_db)
            db.commit()

        print(f"Next Event {event_db.ref_id} | {event_db.name} is created")

    @staticmethod
    def parse_past_event(url: str) -> None:
        r = requests.get(url)
        assert r.status_code == 200

        page = BeautifulSoup(r.content, "html.parser")

        # get event ref_id
        event_ref_id = get_ref_id_from_url(url)

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

        # get fight data (ref_id, pairs)
        fight_data: dict[str, list[tuple[str, str]]] = {}
        trs = page.find_all(
            "tr",
            class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
        )
        for tr in trs:
            fight_ref_url = tr.find_all("a")[0]["href"]
            rows = tr.find_all("a", class_="b-link b-link_style_black")[:2]
            pair = []
            for row in rows:
                fighter_ref_url = row["href"]
                fighter_name = row.get_text(strip=True)
                fighter_data: tuple[str, str] = (fighter_ref_url, fighter_name)
                pair.append(fighter_data)
            fight_data[fight_ref_url] = pair

        db = SessionLocal()

        # save event in db
        event_db = Event(
            name=event_name,
            date=event_date_obj,
            location=event_location,
            ref_url=url,
            ref_id=event_ref_id,
            is_over=True,
        )
        db.add(event_db)
        db.commit()

        # save fights in db
        for fight_ref_url, pair in fight_data.items():
            fight_ref_id = get_ref_id_from_url(fight_ref_url)
            fighter1_ref_url, fighter1_name = pair[0]
            fighter2_ref_url, fighter2_name = pair[1]
            fighter1_ref_id = get_ref_id_from_url(fighter1_ref_url)
            fighter2_ref_id = get_ref_id_from_url(fighter2_ref_url)
            fighter1_db = get_or_create(
                db,
                Fighter,
                ref_id=fighter1_ref_id,
                ref_url=fighter1_ref_url,
                name=fighter1_name,
            )
            fighter2_db = get_or_create(
                db,
                Fighter,
                ref_id=fighter2_ref_id,
                ref_url=fighter2_ref_url,
                name=fighter2_name,
            )
            if not check_does_exist(db, Fight, ref_id=fight_ref_id):
                # For first time parsing (when there is no such fight)
                fight_db = Fight(
                    ref_id=fight_ref_id,
                    ref_url=fight_ref_url,
                    fighter1=fighter1_db,
                    fighter2=fighter2_db,
                    winner=fighter1_db,
                    event=event_db,
                    is_over=True,
                )
            else:
                fight_db = db.query(Fight).filter_by(ref_id=fight_ref_id).first()
            fight_db.winner = fighter1_db
            fight_db.is_over = True

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
        past_event_ref_id = get_ref_id_from_url(past_event_url)
        next_event_ref_id = get_ref_id_from_url(next_event_url)

        if not check_does_exist(db, Event, ref_id=next_event_ref_id):
            self.parse_next_event(next_event_url)
        else:
            print("Skip Next")
        if not check_does_exist(db, Event, ref_id=past_event_ref_id):
            self.parse_past_event(past_event_url)
        else:
            print("Skip Past")

    # def update_next_event(self):
    #     pass
