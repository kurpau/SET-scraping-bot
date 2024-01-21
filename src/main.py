import logging
import os
import sys
import traceback
import urllib.parse
import concurrent.futures

from config import setup_logging
from date_utils import get_date_range
from file_handler import write_to_file
from scraper import Scraper
from user_interaction import clear_cache_if_requested, get_eps_limit

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

    def print_progress(self, completed, total):
        """Prints the progress of a task."""
        progress = (completed / total) * 100
        print(f"Progress: {progress:.2f}% ({completed}/{total})", end="\r", flush=True)

    def fetch_reports(self, stocks):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit a future for each stock's URL
            futures = [
                executor.submit(self.scraper.getReportText, stock["url"])
                for stock in stocks
            ]
            total_stocks = len(stocks)
            completed = 0
            results = []
            for future, stock in zip(concurrent.futures.as_completed(futures), stocks):
                completed += 1
                try:
                    data = future.result()
                    if data is not None:
                        eps = self.scraper.getEPS(data)
                        stock_name = self.scraper.getName(data)
                        stock["stock_name"] = stock_name
                        stock["eps"] = eps
                        results.append(stock)
                except Exception as e:
                    logging.error(f"An error occurred: {e}")

                # Update progress
                self.print_progress(completed, total_stocks)

            print()
            logging.info("All reports fetched.")
            return results

    def start(self):
        try:
            logging.info("Starting script...")

            if os.path.exists("result.txt"):
                os.remove("result.txt")

            stocks_meeting_criteria = 0

            self.scraper.start_browser()
            logging.info("Fetching URLs...")
            html = self.scraper._fetch_dynamic_html()
            stocks = self.scraper.fetch_stocks(html)
            stock_data = self.fetch_reports(stocks)

            # {'url': 'https://www.set.or.th/en/market/news-and-alert/newsdetails?id=85356100&symbol=KSL', 'symbol': 'KSL', 'id': '85356100', 'stock_name': 'ALL INSPIRE DEVELOPMENT PUBLIC COMPANY LIMITED', 'eps': [-0.1, -0.11, -1.06, -0.28]}

            for stock in stock_data:
                try:
                    logging.info(f"Processing stock {stock['symbol']}...")
                    stock_id = stock["id"]
                    stock_name = stock["stock_name"]
                    eps = stock["eps"]

                    if eps is None:
                        logging.warning(
                            f"EPS extraction failed for stock with url: {stock['url']}"
                        )
                        self.cache_manager._write_cache(
                            {stock_id: ([None, None], stock_name)}
                        )
                        continue

                    # Limit to first 2 EPS values (current year)
                    eps = eps[:2]

                    # Write to cache
                    self.cache_manager._write_cache(
                        {stock_id: ([eps[0], eps[1]], stock_name)}
                    )

                    if self.scraper.EPSValid(eps):
                        symbol = stock["symbol"]
                        url = stock["url"]
                        logging.info(
                            f"Stock {stock['symbol']} meets the criteria. Writing to file..."
                        )
                        write_to_file(stock_name, symbol, eps, url)
                        stocks_meeting_criteria += 1

                except Exception as e:
                    logging.error(
                        f"An error occurred while processing stock {stock['symbol']}: {e}"
                    )
                    break

            # After processing all stocks
            if stocks_meeting_criteria == 0:
                logging.warning("No stocks met the criteria. The output file is empty.")
            else:
                logging.info(
                    f'Process finished. {stocks_meeting_criteria} stocks meet the criteria. Check the "result.txt" file.'
                )

            input("Press Enter to continue...")

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            input("Press Enter to continue...")


if __name__ == "__main__":
    eps_limit = get_eps_limit()
    logging.info(f"Using EPS limit of {eps_limit}.")

    from_date, to_date = get_date_range()
    logging.info(f"Date range chosen: from {from_date} to {to_date}")

    clear_cache_if_requested()

    url = construct_url(from_date, to_date)
    main_processor = Main(url, eps_limit)
    main_processor.start()
