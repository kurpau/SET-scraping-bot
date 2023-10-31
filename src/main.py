import requests, re, os, urllib.parse, logging, sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Only error messages will be shown from pyppeteer
logging.getLogger("pyppeteer").setLevel(logging.ERROR)


class Main:
    def __init__(self, url=None):
        self.url = url
        self.limit = 0.02

        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)

        self.output_dir = os.getcwd()

    def _fetch_dynamic_html(self):
        session = HTMLSession()
        response = session.get(self.url)
        response.html.render()
        return response.html.html

    def _get_card_containers(self, soup):
        heading = soup.find("span", string="Today News")
        if not heading:
            logging.error("The 'Today News' heading was not found.")
            exit(1)

        parent_div = heading.find_parent("div", class_="mb-5")
        return parent_div.find_all('div', class_='card-quote-news-contanier')

    def _extract_url_and_symbol(self, container):
        url_element = container.find("a", {"class": "btn-social-facebook"})
        fb_url = url_element["href"]
        parsed_fb_url = urllib.parse.urlparse(fb_url)
        query_params = urllib.parse.parse_qs(parsed_fb_url.query)
        actual_url = query_params["u"][0]

        symbol_element = container.select_one("div.d-flex.flex-column.align-items-center.fs-18px.title-font-family.securities-filed.ps-md-3 > div.me-auto")
        if not symbol_element:
            logging.error("Symbol element not found in container.")
            exit(1)

        symbol = symbol_element.text.strip()
        actual_url += f"&symbol={symbol}"

        return actual_url, symbol

    def get_data(self):
        logging.info("Fetching Data...")
        html = self._fetch_dynamic_html()
        soup = BeautifulSoup(html, "html.parser")
        card_containers = self._get_card_containers(soup)

        results = []
        for container in card_containers:
            actual_url, symbol = self._extract_url_and_symbol(container)
            if actual_url and symbol:
                results.append({"url": actual_url, "symbol": symbol})

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

        stocks_meeting_criteria = (
            0  # Add a counter to keep track of stocks that meet the criteria
        )

        for stock in self.get_data():
            logging.info(f"Processing stock {stock['symbol']}...")
            data = self.getReportText(stock["url"])
            eps = self.getEPS(data)

            if eps is None:
                logging.warning(
                    f"EPS extraction failed for stock with url: {stock['url']}"
                )
                continue

            eps = eps[:2]

            if self.EPSValid(eps):
                name = self.getName(data)
                symbol = stock["symbol"]
                url = stock["url"]
                logging.info(
                    f"Stock {stock['symbol']} meets the criteria. Writing to file..."
                )
                self.WriteToFile(name, symbol, eps, url)
                stocks_meeting_criteria += (
                    1  # Increment the counter if a stock meets the criteria
                )

        if stocks_meeting_criteria == 0:
            logging.warning("No stocks met the criteria. The output file is empty.")
        else:
            logging.info('Process finished. Check the "result.txt" file.')


if __name__ == "__main__":
    url = "https://www.set.or.th/en/market/news-and-alert/news?source=company&securityType=S&type=3&keyword=F45"
    main = Main(url)
    main.Start()
