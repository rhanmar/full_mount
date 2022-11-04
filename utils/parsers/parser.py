# from utils.parsers.mock_data import MOCK_DATA_EVENTS
import requests
from bs4 import BeautifulSoup

url_list_events = (
    "http://www.ufcstatsapi.com/events/?skip=0&limit=100&date_descending=true"
)
url_detail_events = "http://www.ufcstatsapi.com/events/{}"
url__list_fights = (
    "http://www.ufcstatsapi.com/fights/?skip=0&limit=10&date_descending=true"
)

url_ufc_stats = "http://ufcstats.com/statistics/events/completed"
url_rod_lemos = "http://www.ufcstats.com/event-details/756f45905fb20cb5"


# r = requests.get(url_rod_lemos)
#
# page = BeautifulSoup(r.content, "html.parser")
#
# pairs = []
#
# trs = page.find_all(
#     "tr",
#     class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click",
# )
# for tr in trs:
#     rows = tr.find_all("a", class_="b-link b-link_style_black")[:2]
#     pair = []
#     for row in rows:
#         print(row.get_text(strip=True))
#         pair.append(row.get_text(strip=True))
#     pairs.append(pair)
#
# print(pairs)


def get_next_event():
    r = requests.get(url_list_events)
    assert r.status_code == 200


    from db.models import Event, Fight, Fighter
    from db.database import SessionLocal
    from datetime import datetime

    r_json = r.json()
    next_event_json = r_json[0]
    db = SessionLocal()

    does_exist = db.query(Event).filter(Event.name == next_event_json["event_name"]).count()
    print(does_exist)
    print(does_exist)
    print(does_exist)
    if does_exist:
        return None

    # time_json = next_event_json["event_date"].split("T")[0]
    # time = datetime.strptime(time_json, "%Y-%m-%d")

    next_event = Event(
        name=next_event_json["event_name"],
        # date=time,
        date=next_event_json["event_date"],
        location=next_event_json["event_location"],
        url=next_event_json["event_url"]
    )
    db.add(next_event)
    db.commit()

    r = requests.get(next_event.url)
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
            print(row.get_text(strip=True))
            pair.append(row.get_text(strip=True))
        pairs.append(pair)

    print(pairs)

    for fighter1, fighter2 in pairs:
        fighter1_db = Fighter(name=fighter1)
        fighter2_db = Fighter(name=fighter2)
        fight_db = Fight(
            fighter1=fighter1_db,
            fighter2=fighter2_db,
            event=next_event
        )
        db.add(fighter1_db)
        db.add(fighter2_db)
        db.add(fight_db)
        db.commit()



