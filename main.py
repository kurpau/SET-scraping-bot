import requests, re, os, urllib.parse, logging, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('selenium').setLevel(logging.WARNING)

class Main:
    def __init__(self, url):
        self.url = url
        self.limit = 0.02

        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)
        
        self.output_dir = os.getcwd()


    def get_data(self):
        logging.info("Starting the Selenium WebDriver...")
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        container_elements = soup.find_all('div', {'class': 'card-quote-news-contanier'})

        results = []

        for container in container_elements:
            url_element = container.find('a', {'class': 'btn-social-facebook'})
            fb_url = url_element['href']

            parsed_fb_url = urllib.parse.urlparse(fb_url)
            query_params = urllib.parse.parse_qs(parsed_fb_url.query)
            actual_url = query_params['u'][0]

            symbol_element = container.find('div', {'class': 'symbol-quote'})
            symbol = symbol_element.text.strip()

            actual_url += f"&symbol={symbol}"

            results.append({'url': actual_url, 'symbol': symbol})

        driver.quit()
        logging.info("Fetched stock data. Processing stocks...")
        return results

    def getReportText(self, link):
        try:
            # Get page HTML content
            html_doc = requests.get(link).content
        except RequestException as e:
            logging.error(f"Failed to fetch HTML content from {link}")
            logging.debug(f"Exception details: {e}")
            return None

        try:
            soup = BeautifulSoup(html_doc, 'html.parser')
            # Get report in text format
            s = soup.pre.text
            # Remove whitespace and breaks from text
            s = ' '.join(s.split())
            return s
        except AttributeError as e:
            logging.error(f"Failed to extract report text from {link}")
            logging.debug(f"Exception details: {e}")
            return None

    def getName(self, data):
        try:
            name = re.search('\(F45\)(.*)\(In', data).group(1)
            return name.strip()
        except AttributeError as e:
            logging.debug("Failed to extract EPS values: RE pattern not found")
            logging.debug(f"Exception details: {e}")
            return None

    def getEPS(self, data):
        try:
            # Find the line containing EPS values
            line = re.search('EPS \(baht\) (.*)Remark', data).group(1)

            # Regular expression for matching EPS values (with named groups)
            eps_pattern = r'\(?(?P<value>\d[\d.,]*)(?P<negative>\)?)'
            eps_matches = re.finditer(eps_pattern, line)

            # Extract and clean EPS values
            EPS = []
            for match in eps_matches:
                eps = match.group('value').replace(",", "")
                if match.group('negative'):
                    EPS.append(-float(eps))
                else:
                    EPS.append(float(eps))

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
        file_path = os.path.join(self.output_dir, 'result.txt')
        with open(file_path, 'a') as f:
            f.write(f'{name} [ {ticker} ] \n')
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

        for stock in self.get_data():
            logging.info(f"Processing stock {stock['symbol']}...")
            data = self.getReportText(stock['url'])
            eps = self.getEPS(data)
    
            if eps is None:
                logging.warning(f"EPS extraction failed for stock with url: {stock['url']}")
                continue
                
            eps = eps[:2]

            if self.EPSValid(eps):
                name = self.getName(data)
                symbol = stock['symbol']
                url = stock['url']
                logging.info(f"Stock {stock['symbol']} meets the criteria. Writing to file...")
                self.WriteToFile(name, symbol, eps, url)
        logging.info("Process finished. Check the \"result.txt\" file.")

if __name__ == "__main__":
    url = "https://www.set.or.th/en/market/news-and-alert/news?source=company&securityType=S&type=3&keyword=F45"
    main = Main(url)
    main.Start()
