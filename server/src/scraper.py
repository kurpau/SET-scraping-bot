import logging
import os
import re
import urllib.parse
import requests_cache
import datetime
import concurrent.futures

# import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class Scraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.cache_duration = datetime.timedelta(
            hours=1
        )  # Duration for which the cache is valid
        requests_cache.install_cache("stock_cache", expire_after=self.cache_duration)

    def start_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.webkit.launch(headless=False)
        self.page = self.browser.new_page()

    def close_browser(self):
        self.browser.close()
        self.playwright.stop()

    def _get_card_containers(self, soup):
        heading = soup.find(
            "span", string=lambda t: t is not None and "Search Result" in t.strip()
        )
        if not heading:
            logging.error(
                f"No search results found. Check this URL to confirm: {self.url}"
            )
            exit(1)

        parent_div = heading.find_parent("div", class_="mb-5")
        return parent_div.find_all("div", class_="card-quote-news-contanier")

    def _extract_params(self, container):
        url_element = container.find("a", {"class": "btn-social-facebook"})
        fb_url = url_element["href"]
        parsed_fb_url = urllib.parse.urlparse(fb_url)
        query_params = urllib.parse.parse_qs(parsed_fb_url.query)
        actual_url = query_params["u"][0]

        parsed_actual_url = urllib.parse.urlparse(actual_url)
        stock_id = urllib.parse.parse_qs(parsed_actual_url.query).get("id", [None])[0]

        if not stock_id:
            logging.error("ID not found in the URL.")
            exit(1)

        symbol_element = container.select_one(
            "div.d-flex.flex-column.align-items-center.fs-18px.title-font-family.securities-filed.ps-md-3 > div.me-auto"
        )
        if not symbol_element:
            logging.error("Symbol element not found in container.")
            exit(1)

        symbol = symbol_element.text.strip()
        actual_url += f"&symbol={symbol}"

        return (
            actual_url,
            symbol,
            stock_id,
        )

    def set_dropdown_value(self, level):
        levels = {1: 10, 2: 20, 3: 30, 4: 50, 5: 100}
        self.page.locator(".multiselect__select").first.click()
        self.page.locator(f"li:nth-child({level}) > .multiselect__option").first.click()
        logging.debug(f"Dropdown value set to {levels[level]} results per page")

    def get_max_pages(self):
        li_elements = self.page.locator("ul.pagination li")
        second_last_li = li_elements.nth(-2)
        return int(second_last_li.inner_text().strip())

    def fetch_stocks(self, url):
        self.start_browser()
        self.page.goto(url)
        self.get_max_pages()

        results = []
        page = 1

        self.set_dropdown_value(5)
        max_pages = self.get_max_pages()
        next_button = self.page.get_by_label("Go to next page")
        logging.info("Fetching Stocks...")
        while next_button:
            self.page.wait_for_selector('text="Search Result"')
            html = self.page.content()
            soup = BeautifulSoup(html, "html.parser")
            card_containers = self._get_card_containers(soup)

            next_button = self.page.get_by_label("Go to next page")

            for container in card_containers:
                actual_url, symbol, stock_id = self._extract_params(container)
                if actual_url and symbol:
                    results.append(
                        {"url": actual_url, "symbol": symbol, "id": stock_id}
                    )
            self.print_progress(page, max_pages, "Scraping Pages")

            next_button = self.page.get_by_label("Go to next page")
            if next_button and next_button.is_disabled():
                logging.debug(
                    f"The 'next' button is disabled, [{page}] was the last page."
                )
                break
            else:
                next_button.click()
                page += 1

        print()
        logging.info(f"{len(results)} Stocks found!")
        self.close_browser()
        results = self.fetch_reports(results)
        return results

    def fetch_reports(self, stocks):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit a future for each stock's URL and store in a dictionary
            future_to_stock = {
                executor.submit(self.getReportText, stock["url"]): stock
                for stock in stocks
            }
            total_stocks = len(stocks)
            completed = 0
            results = []
            for future in concurrent.futures.as_completed(future_to_stock):
                stock = future_to_stock[future]
                completed += 1
                data = future.result()
                if data is not None:
                    eps = self.getEPS(data)
                    stock_name = self.getName(data)
                    stock["stock_name"] = stock_name
                    stock["eps"] = eps
                    results.append(stock)

                self.print_progress(completed, total_stocks, "Fetching Reports")

        print()
        logging.info("All reports fetched.")
        return results

    def print_progress(self, completed, total, message):
        """Prints the progress of a task."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"{current_time} - INFO - {message}: ({completed}/{total})",
            end="\r",
            flush=True,
        )

    def getReportText(self, link):
        # Use the requests_cache session to get the page content
        with requests_cache.CachedSession(expire_after=self.cache_duration) as session:
            try:
                # Get page HTML content
                response = session.get(link)
                response.raise_for_status()  # Check for HTTP request errors
                html_doc = response.content
            except Exception as e:
                logging.error(f"Failed to fetch HTML content from {link}")
                logging.debug(f"Exception details: {e}")
                return None

            try:
                soup = BeautifulSoup(html_doc, "html.parser")
                # Get report in text format
                report_text = soup.pre.text
                # Remove whitespace and breaks from text
                report_text = " ".join(report_text.split())
                return report_text
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

            return EPS[:2]

        except AttributeError as e:
            logging.debug("Failed to extract EPS values: RE pattern not found")
            logging.debug(f"Exception details: {e}")
            return None

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
