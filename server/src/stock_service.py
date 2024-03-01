from datetime import datetime
import urllib.parse


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class StockService:
    def __init__(self, scraper):
        self.scraper = scraper

    def fetch_stocks(self, from_date_str, to_date_str):
        if not is_valid_date(from_date_str) or not is_valid_date(to_date_str):
            raise ValueError("Invalid date format, expected YYYY-MM-DD.")
        query_url = self.construct_url(from_date_str, to_date_str)
        urls = self.scraper.scrape_report_urls(query_url)
        return self.scraper.fetch_reports(urls)

    def construct_url(self, from_date_str=None, to_date_str=None):
        from_date = (
            datetime.strptime(from_date_str, "%Y-%m-%d")
            if from_date_str
            else datetime.today()
        )
        to_date = (
            datetime.strptime(to_date_str, "%Y-%m-%d")
            if to_date_str
            else datetime.today()
        )

        url_params = {
            "source": "company",
            "securityType": "S",
            "type": "3",
            "keyword": "F45",
            "fromDate": from_date.strftime("%Y-%m-%d"),
            "toDate": to_date.strftime("%Y-%m-%d"),
        }
        return f"https://www.set.or.th/en/market/news-and-alert/news?{urllib.parse.urlencode(url_params)}"
