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


r = requests.get(url_rod_lemos)

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
