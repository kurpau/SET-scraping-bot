import requests, re, os
from bs4 import BeautifulSoup

class Main:
    def __init__(self):
        pass

    def get_data(self):
        try: 
            api_url = "https://www.set.or.th/api/set/news/search?keyword=F45&lang=en"
            r = requests.get(api_url)
            print("Fetching data...")
        except requests.exceptions.HTTPError as err:
            print("SET server ERROR: \n")
            raise SystemExit(err)
        
        data = r.json()["newsInfoList"]
        if data:
            print("Processing data...")
            return data
        else:
            raise SystemExit("Server returned no data")


    def getReportText(self, link):
        # Get page HTML content
        html_doc = requests.get(link).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Get report in text format
        s = soup.pre.text
        # Remove whitespace and breaks from text
        s = ' '.join(s.split())
        return s

    def getName(self, data):
        try:
            name = re.search('\(F45\)(.*)\(In', data).group(1)
            return name.strip()
        except AttributeError:
            print("RE pattern not found")

    def getEPS(self, data):
        try:
            # List to store EPS values
            EPS = []
            # Get a text line in report where EPS numbers are present
            line = re.search('EPS \(baht\) (.*)Remark', data).group(1) # "Remark" instead of "Type" for (Unoudited) report supporrt
            # Clean up text line from non EPS strings
            r = re.compile(r'(\(?\d[\d.,]*\)?)')
            for eps in re.findall(r, line):
                eps = eps.replace(",", "") # fixes error when decimal comma is used in the report
                # Check if number should be negative
                if '(' in eps:
                    # Append string to EPS list and convert it to a negative float
                    EPS.append(-float(eps.translate(str.maketrans('','','()'))))
                else:
                    # Append string to EPS list and convert it to float
                    EPS.append(float(eps))
            return EPS
        # Handle regex errors
        except AttributeError:
            print("RE pattern not found")

    def EPSValid(self, eps_list):
        curr_eps = eps_list[0]
        prev_eps = eps_list[1]
        limit = 0.02
        if curr_eps > 0 and prev_eps > 0 and (curr_eps - prev_eps >= limit):
            return True
        return False
    
    def WriteToFile(self, name, ticker, eps_list, url):
        with open('result.txt', 'a') as f:
            f.write(f'{name} [ {ticker} ] \n')
            f.write('|' + '-' * 21 + '|\n')
            f.write("| {:<8} | {:<8} | \n".format('Current','Previous'))
            f.write('|' + '-' * 21 + '|\n')
            f.write("| {:>8} | {:>8} | \n".format(eps_list[0], eps_list[1]))
            f.write('|' + '-' * 21 + '|\n')
            f.write("Link to F45 page: " + url + '\n')
            f.write("\n")


    def Start(self):
        try:
            os.remove("result.txt")
        except OSError:
            pass

        for stock in self.get_data():
            data = self.getReportText(stock['url'])
            eps = self.getEPS(data)[:2]
            if self.EPSValid(eps):
                name = self.getName(data)
                symbol = stock['symbol']
                url = stock['url']
                self.WriteToFile(name, symbol, eps, url)
        print("Process finished")

if __name__ == "__main__":
    main = Main()
    main.Start()
