# Investing.com economic calendar scraper

## How to run

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ./main.py 2010-01-01 2024-06-19
```

## How I built this

1. Inspect https://www.investing.com/economic-calendar/ with Chrome Dev Tool
1. Since it is a infinite scroll website, there should be an API for the frontend to call
1. Found the API at `/economic-calendar/Service/getCalendarFilteredData`
1. Use `dateFrom` and `dateTo` to request data from a time range.
1. Use `limitFrom` to loop through the pagination
1. The response from the API is a JSON, but the actual data is rendered in HTML
1. Handle invalid data such as date separators and holiday

## TODO

1. Scale the scraper
   1. Modular design, separate network request, parsing, and storage.
   1. Communicate via task queues
1. Data integrity check
1. Retry and resume from failed jobs
1. Stream processing instead of bulk
