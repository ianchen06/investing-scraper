import datetime
import argparse


def get_config():
    parser = argparse.ArgumentParser(
        description="Scrapes Investing.com for economic calendar data."
    )
    parser.add_argument(
        "start_date",
        help="Start date. e.g. 2010-01-01 ",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
    )
    parser.add_argument(
        "end_date",
        help="End date. e.g. 2024-06-18",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
    )
    return parser.parse_args()
