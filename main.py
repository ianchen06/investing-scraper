from scraper import Scraper
from config import get_config


if __name__ == "__main__":
    config = get_config()
    scraper = Scraper()
    scraper.run(config.start_date, config.end_date)
