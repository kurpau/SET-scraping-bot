import logging
import os, sys, urllib.parse
from user_interaction import get_eps_limit, clear_cache_if_requested
from date_utils import get_date_range
from scraper import Scraper
from config import output_dir
from cache_manager import CacheManager
from file_handler import write_to_file


def construct_url(from_date, to_date):
    from_date_str = from_date.strftime('%Y-%m-%d')
    to_date_str = to_date.strftime('%Y-%m-%d')
    url_params = {
        "source": "company",
        "securityType": "S",
        "type": "3",
        "keyword": "F45",
        "fromDate": from_date_str,
        "toDate": to_date_str
    }
    url = f"https://www.set.or.th/en/market/news-and-alert/news?{urllib.parse.urlencode(url_params)}"

    return url

class Main:
    def __init__(self, url=None, eps_limit=0.02):
        self.url = url
        self.scraper = Scraper(url, eps_limit)
        self.cache_manager = CacheManager()

        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)

        self.output_dir = os.getcwd()

    def start(self):
        logging.info("Starting script...")

        if os.path.exists("result.txt"):
            os.remove("result.txt")

        stocks_meeting_criteria = 0  # Add a counter to keep track of stocks that meet the criteria

        # Read cache once outside the loop to avoid reading the file multiple times
        cache = self.cache_manager._read_cache()

        for stock in self.scraper.get_data():
            logging.info(f"Processing stock {stock['symbol']}...")
            stock_id = stock['id']
            if stock_id not in cache:
                data = self.scraper.getReportText(stock["url"])

                eps = self.scraper.getEPS(data)

                if eps is None:
                    logging.warning(
                        f"EPS extraction failed for stock with url: {stock['url']}"
                    )
                    continue

                # Limit to first 2 EPS values
                eps = eps[:2]
                stock_name = self.scraper.getName(data)

                # Write to cache
                self.cache_manager._write_cache({stock_id: ([eps[0], eps[1]], stock_name)})
            else:
                # If it's in cache, use cached values
                eps = cache[stock_id][0]
                stock_name = cache[stock_id][1]
                logging.info(f"Stock [{stock['symbol']}] already processed before, using EPS from cache: {eps}")

            if self.scraper.EPSValid(eps):
                symbol = stock["symbol"]
                url = stock["url"]
                logging.info(
                    f"Stock {stock['symbol']} meets the criteria. Writing to file..."
                )
                write_to_file(stock_name, symbol, eps, url)
                stocks_meeting_criteria += 1

        if stocks_meeting_criteria == 0:
            logging.warning("No stocks met the criteria. The output file is empty.")
        else:
            logging.info('Process finished. Check the "result.txt" file.')

if __name__ == "__main__":
    eps_limit = get_eps_limit()
    logging.info(f"Using EPS limit of {eps_limit}.")

    from_date, to_date = get_date_range()
    logging.info(f"Date range chosen: from {from_date} to {to_date}")

    clear_cache_if_requested()

    url = construct_url(from_date, to_date)
    main_processor = Main(url, eps_limit)
    main_processor.start()

