from filecmp import clear_cache
import requests, re, os, urllib.parse, logging, sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Only error messages will be shown from pyppeteer
logging.getLogger("pyppeteer").setLevel(logging.ERROR)


class Main:
    def __init__(self, url=None, eps_limit=0.02):
        self.url = url
        self.limit = eps_limit

        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)

        self.output_dir = os.getcwd()

    def _write_cache(self, cache):
        cache_path = os.path.join(self.output_dir, "cache.txt")
        with open(cache_path, "a") as f:
            for stock_id, eps_values in cache.items():
                f.write(f"{stock_id}|{eps_values[0]}|{eps_values[1]}\n")

    def _read_cache(self):
        cache_path = os.path.join(self.output_dir, "cache.txt")
        if not os.path.exists(cache_path):
            return {}
        with open(cache_path, "r") as f:
            data = f.readlines()
        cache = {}
        for line in data:
            stock_id, curr_eps, prev_eps = line.strip().split("|")
            cache[stock_id] = [float(curr_eps), float(prev_eps)]
        return cache


    def _fetch_dynamic_html(self):
        session = HTMLSession()
        response = session.get(self.url)
        response.html.render(timeout=16)
        return response.html.html

    def _get_card_containers(self, soup):
        heading = soup.find("span", string=lambda t: t is not None and "Search Result" in t.strip())
        if not heading:
            logging.error("The 'Search Result' heading was not found.")
            exit(1)

        parent_div = heading.find_parent("div", class_="mb-5") # TODO: handle for all not found cases
        return parent_div.find_all('div', class_='card-quote-news-contanier')


    def _extract_params(self, container):
        url_element = container.find("a", {"class": "btn-social-facebook"})
        fb_url = url_element["href"]
        parsed_fb_url = urllib.parse.urlparse(fb_url)
        query_params = urllib.parse.parse_qs(parsed_fb_url.query)
        actual_url = query_params["u"][0]

        parsed_actual_url = urllib.parse.urlparse(actual_url)
        stock_id = urllib.parse.parse_qs(parsed_actual_url.query).get('id', [None])[0]

        if not stock_id:
            logging.error("ID not found in the URL.")
            exit(1)
            
        symbol_element = container.select_one("div.d-flex.flex-column.align-items-center.fs-18px.title-font-family.securities-filed.ps-md-3 > div.me-auto")
        if not symbol_element:
            logging.error("Symbol element not found in container.")
            exit(1)

        symbol = symbol_element.text.strip()
        actual_url += f"&symbol={symbol}"

        return actual_url, symbol, stock_id  # Returning id along with actual_url and symbol


    def get_data(self):
        logging.info("Fetching Data...")
        html = self._fetch_dynamic_html()
        soup = BeautifulSoup(html, "html.parser")
        card_containers = self._get_card_containers(soup)

        results = []
        for container in card_containers:
            actual_url, symbol, stock_id = self._extract_params(container)
            if actual_url and symbol:
                results.append({"url": actual_url, "symbol": symbol, "id": stock_id})

        logging.info("Fetched stock data. Processing stocks...")
        return results

    def getReportText(self, link):
        try:
            # Get page HTML content
            html_doc = requests.get(link).content
        except Exception as e:
            logging.error(f"Failed to fetch HTML content from {link}")
            logging.debug(f"Exception details: {e}")
            return None

        try:
            soup = BeautifulSoup(html_doc, "html.parser")
            # Get report in text format
            s = soup.pre.text
            # Remove whitespace and breaks from text
            s = " ".join(s.split())
            return s
        except AttributeError as e:
            logging.error(f"Failed to extract report text from {link}")
            logging.debug(f"Exception details: {e}")
            return None

    def getName(self, data):
        try:
            name = re.search(r"\(F45\)(.*)\(In", data).group(1)
            return name.strip()
        except AttributeError as e:
            logging.debug("Failed to extract EPS values: RE pattern not found")
            logging.debug(f"Exception details: {e}")
            return None

    def getEPS(self, data):
        try:
            # Find the line containing EPS values
            line = re.search(r"EPS \(baht\) ([^\n]*)", data).group(1)

            # Regular expression for matching EPS values (with named groups)
            eps_pattern = r"\(?(?P<value>\d[\d.,]*)(?P<negative>\)?)"
            eps_matches = re.finditer(eps_pattern, line)

            # Extract and clean EPS values
            EPS = []
            for match in eps_matches:
                eps = match.group("value").replace(",", "")
                if match.group("negative"):
                    EPS.append(-float(eps))
                else:
                    EPS.append(float(eps))

            if not EPS:
                return None

            return EPS

        except AttributeError as e:
            logging.debug("Failed to extract EPS values: RE pattern not found")
            logging.debug(f"Exception details: {e}")
            return None

    def EPSValid(self, eps_list):
        curr_eps = eps_list[0]
        prev_eps = eps_list[1]
        if curr_eps > 0 and prev_eps > 0 and (curr_eps - prev_eps >= self.limit):
            return True
        return False

    def WriteToFile(self, name, ticker, eps_list, url):
        file_path = os.path.join(self.output_dir, "result.txt")
        with open(file_path, "a") as f:
            f.write(f"{name} [ {ticker} ] \n")
            f.write(f'|{"-" * 21}|\n')
            f.write(f"| {'Current':<8} | {'Previous':<8} | \n")
            f.write(f'|{"-" * 21}|\n')
            f.write(f"| {eps_list[0]:>8} | {eps_list[1]:>8} | \n")
            f.write(f'|{"-" * 21}|\n')
            f.write(f"Link to F45 page: {url}\n\n")

    def Start(self):
        logging.info("Starting script...")

        if os.path.exists("result.txt"):
            os.remove("result.txt")

        stocks_meeting_criteria = 0  # Add a counter to keep track of stocks that meet the criteria

        # Read cache once outside the loop to avoid reading the file multiple times
        cache = self._read_cache()

        for stock in self.get_data():
            logging.info(f"Processing stock {stock['symbol']}...")
            stock_id = stock['id']
            if stock_id not in cache:
                data = self.getReportText(stock["url"])

                eps = self.getEPS(data)

                if eps is None:
                    logging.warning(
                        f"EPS extraction failed for stock with url: {stock['url']}"
                    )
                    continue

                # Limit to first 2 EPS values
                eps = eps[:2]

                # Write to cache
                self._write_cache({stock_id: [eps[0], eps[1]]})
            else:
                # If it's in cache, use cached values
                eps = cache[stock_id]
                logging.info(f"Stock [{stock['symbol']}] already processed before, using EPS from cache: {eps}")

            if self.EPSValid(eps):
                name = self.getName(data) if 'data' in locals() else "Unknown Name"  # Fetch name if 'data' exists, else default to "Unknown Name"
                symbol = stock["symbol"]
                url = stock["url"]
                logging.info(
                    f"Stock {stock['symbol']} meets the criteria. Writing to file..."
                )
                self.WriteToFile(name, symbol, eps, url)
                stocks_meeting_criteria += 1

        if stocks_meeting_criteria == 0:
            logging.warning("No stocks met the criteria. The output file is empty.")
        else:
            logging.info('Process finished. Check the "result.txt" file.')



if __name__ == "__main__":
    import datetime

    def get_today():
        return datetime.date.today(), datetime.date.today()

    def get_yesterday():
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        return yesterday, yesterday

    def get_last_5_days():
        return datetime.date.today() - datetime.timedelta(days=5), datetime.date.today()

    def get_last_month():
        return datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()

    def get_last_3_months():
        return datetime.date.today() - datetime.timedelta(days=90), datetime.date.today()

    def get_date_range():
        date_range_switcher = {
            '1': get_today,
            '2': get_yesterday,
            '3': get_last_5_days,
            '4': get_last_month,
            '5': get_last_3_months
        }
        user_choice = input("Select date period: 1. Today 2. Yesterday 3. Last 5 days 4. Last month 5. Last 3 months: ")
        date_range_func = date_range_switcher.get(user_choice, get_today)
        return date_range_func()

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

    # Prompt the user for EPS limit
    while True:
        try:
            user_input = input("Enter the EPS limit (default is 0.02 or type 'exit' to quit): ")
            
            if user_input.lower() == 'exit':
                logging.info("Exiting script.")
                sys.exit(0)
                
            eps_limit = float(user_input) if user_input else 0.02
            break
        except ValueError:
            logging.info("Invalid input. Please enter a valid number for EPS limit or type 'exit' to quit.")

    logging.info(f"Using EPS limit of {eps_limit}.")

    from_date, to_date = get_date_range()
    logging.info(f"Date chosen: {from_date} - {to_date}")

    clear_cache = input("Would you like to erase cached data? [y]/[n] ").lower()
    if clear_cache == "y":
        # Clear the cache file
        cache_path = os.path.join(os.getcwd(), "cache.txt")
        if os.path.exists(cache_path):
            os.remove(cache_path)
        logging.info("Cache cleared!")

    url = construct_url(from_date, to_date)
    main = Main(url, eps_limit)
    main.Start()

