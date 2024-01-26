import logging
import os
import sys
import traceback
import urllib.parse

from config import setup_logging
from date_utils import get_date_range
from file_handler import write_to_file
from scraper import Scraper
from user_interaction import get_eps_limit

setup_logging()


def construct_url(from_date, to_date):
    from_date_str = from_date.strftime("%Y-%m-%d")
    to_date_str = to_date.strftime("%Y-%m-%d")
    url_params = {
        "source": "company",
        "securityType": "S",
        "type": "3",
        "keyword": "F45",
        "fromDate": from_date_str,
        "toDate": to_date_str,
    }
    url = f"https://www.set.or.th/en/market/news-and-alert/news?{urllib.parse.urlencode(url_params)}"

    return url


class Main:
    def __init__(self, url=None, eps_limit=0.02):
        self.url = url
        self.scraper = Scraper(url, eps_limit)

        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)

        self.output_dir = os.getcwd()

    def start(self):
        logging.info("Starting script...")

        if os.path.exists("result.txt"):
            os.remove("result.txt")

        stocks_meeting_criteria = 0

        try:
            self.scraper.start_browser()
            logging.info("Fetching Stocks...")
            html = self.scraper._fetch_dynamic_html()
            stocks = self.scraper.fetch_stocks(html)
            stock_data = self.scraper.fetch_reports(stocks)

            for stock in stock_data:
                stock_name = stock.get("stock_name")
                eps = stock.get("eps")
                symbol = stock.get("symbol")
                url = stock.get("url")

                if not stock_name or not eps:
                    logging.warning(
                        f"Skipping stock {symbol} with url: {url} due to missing data"
                    )
                    continue

                if self.scraper.EPSValid(eps):
                    write_to_file(stock_name, symbol, eps, url)
                    stocks_meeting_criteria += 1

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            traceback.print_exc()
        finally:
            self.scraper.close_browser()

        # After processing all stocks
        if stocks_meeting_criteria == 0:
            logging.warning("No stocks met the criteria. The output file is empty.")
        else:
            logging.info(
                f'Process finished. {stocks_meeting_criteria} stocks meet the criteria. Check the "result.txt" file.'
            )

        input("Press Enter to continue...")


if __name__ == "__main__":
    eps_limit = get_eps_limit()
    logging.info(f"Using EPS limit of {eps_limit}.")

    from_date, to_date = get_date_range()
    logging.info(f"Date range chosen: from {from_date} to {to_date}")

    url = construct_url(from_date, to_date)
    main_processor = Main(url, eps_limit)
    main_processor.start()
