import logging
import os
import re
import urllib.parse
import requests_cache
import datetime

# import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class Scraper:
    def __init__(self, url, eps_limit):
        self.url = url
        self.limit = eps_limit
        self.playwright = None
        self.browser = None
        self.page = None
        self.cache_duration = datetime.timedelta(
            hours=1
        )  # Duration for which the cache is valid
        requests_cache.install_cache("stock_cache", expire_after=self.cache_duration)

    def start_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.webkit.launch()
        self.page = self.browser.new_page()

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.playwright.stop()

    def _fetch_dynamic_html(self):
        if not self.page:  # If page is not initialized, start the browser
            self.start_browser()

        self.page.goto(self.url)
        content = self.page.content()
        return content

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
        )  # Returning id along with actual_url and symbol

    def set_dropdown_value(self, level):
        levels = {1: 10, 2: 20, 3: 30, 4: 50, 5: 100}
        self.page.locator(".multiselect__select").first.click()
        self.page.locator(f"li:nth-child({level}) > .multiselect__option").first.click()
        logging.info(f"Dropdown value set to {levels[level]} results per page")

    def fetch_stocks(self, html):
        results = []
        i = 1

        self.set_dropdown_value(5)
        next_button = self.page.get_by_label("Go to next page")
        while next_button:
            soup = BeautifulSoup(html, "html.parser")
            card_containers = self._get_card_containers(soup)

            next_button = self.page.get_by_label("Go to next page")

            for container in card_containers:
                actual_url, symbol, stock_id = self._extract_params(container)
                if actual_url and symbol:
                    results.append(
                        {"url": actual_url, "symbol": symbol, "id": stock_id}
                    )
            logging.info(f"Results fetched for page [{i}]")

            next_button = self.page.get_by_label("Go to next page")
            if next_button and next_button.is_disabled():
                logging.info(f"The 'next' button is disabled, [{i}] was the last page.")
                break
            else:
                # press the button
                next_button.click()
                self.page.wait_for_selector('text="Search Result"')
                html = self.page.content()
                i += 1

        logging.info(f"{len(results)} Stocks found!")
        return results

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
