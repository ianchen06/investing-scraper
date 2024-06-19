import json
import uuid

import requests
from bs4 import BeautifulSoup
import pandas as pd


class Scraper:
    def __init__(self):
        self.base_url = "https://www.investing.com"
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.investing.com",
            "priority": "u=1, i",
            "referer": "https://www.investing.com/economic-calendar/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        self.payload = {
            "country[]": "5",  # USA
            "dateFrom": "2010-01-01",
            "dateTo": "2024-06-16",
            "timeZone": "8",  # US/Eastern
            "timeFilter": "timeRemain",
            "currentTab": "custom",
            "limit_from": "0",
            "submitFilters": "0",
            "last_time_scope": "0",
            "byHandler": "true",
        }

    def scrape(self, start_date, end_date):
        self.run_id = uuid.uuid4()
        db = []
        page = 0
        self.payload["dateFrom"] = start_date.strftime("%Y-%m-%d")
        self.payload["dateTo"] = end_date.strftime("%Y-%m-%d")

        print(self.payload)

        try:
            while True:
                print(f"Scraping page {page}")
                response = requests.post(
                    self.base_url
                    + "/economic-calendar/Service/getCalendarFilteredData",
                    headers=self.headers,
                    data=self.payload,
                )
                if not response:
                    break
                if "No Events" in response.json()["data"]:
                    break
                db.append(response.json())
                page += 1
                self.payload["limit_from"] = page
        finally:
            json.dump(db, open(f"./{self.run_id}.json", "w"))

    def extract(self):
        print(f"Extracting data from {self.run_id}.json")
        htmls = json.load(open(f"./{self.run_id}.json"))
        self.parsed_data = []
        for html in htmls:
            soup = BeautifulSoup(html["data"])
            for row in soup.select("tr"):
                cols = row.select("td")
                if """Holiday""" in row.text:
                    continue
                # skip data seperator
                if len(cols) == 1:
                    continue
                data = {}
                data["dt"] = row["data-event-datetime"]
                data["currency"] = cols[1].get_text().split(" ")[1]
                data["importance"] = len(cols[2].select("i.grayFullBullishIcon"))
                a_url = cols[3].select_one("a")
                data["url"] = self.base_url + a_url["href"]
                data["event"] = a_url.get_text().strip()
                data["actual"] = cols[4].get_text().strip()
                data["forecase"] = cols[5].get_text().strip()
                data["previous"] = cols[6].get_text().strip()
                self.parsed_data.append(data)

    def store(self):
        print(f"Storing data to {self.run_id}.csv")
        df = pd.DataFrame(self.parsed_data)
        df.to_csv(f"./{self.run_id}.csv", index=False)

    def run(self, start_date, end_date):
        self.scrape(start_date, end_date)
        self.extract()
        self.store()
