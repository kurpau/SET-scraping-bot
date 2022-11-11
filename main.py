import requests
from bs4 import BeautifulSoup
import re
import os

class Main:
    def __init__(self):
        pass

    def get_links(self):
        # List for storing links
        links = []
        link_prefix = "https://classic.set.or.th/"
        URL = "https://classic.set.or.th/set/searchtodaynews.do?newsGroupId=3&language=en&country=US"
        # Get page HTML content
        html_doc = requests.get(URL).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Find second table on the page
        second_table = soup.findAll('table')[1]
        # Find table body
        table_body = second_table.find('tbody')
        # Find table rows
        rows = table_body.find_all('tr')
        # Loop through rows
        for row in rows:
            cols = row.find_all('td')
            # Check if it's the correct financial report
            if "(F45)" in cols[-2].text:
                # Get relative link to report page
                rel_link = cols[-1].find('a').attrs['href']
                # Get ticker
                ticker = cols[-4].text
                # Add link prefix to relative link and append to link list
                links.append({'link': str(link_prefix + rel_link), 'ticker': ticker})
        
        return links

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
            return name
        except AttributeError:
            print("RE pattern not found")

    def getEPS(self, data):
        try:
            # List to store EPS values
            EPS = []
            # Get a text line in report where EPS numbers are present
            line = re.search('EPS \(baht\) (.*)Type', data).group(1)
            print(line)
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
    
    def WriteToFile(self, name, ticker, eps_list):
        with open('result.txt', 'a') as f:
            f.write(f'{name} [ {ticker} ] \n')
            f.write('|' + '-' * 21 + '|\n')
            f.write("| {:<8} | {:<8} | \n".format('Current','Previous'))
            f.write('|' + '-' * 21 + '|\n')
            f.write("| {:>8} | {:>8} | \n".format(eps_list[0], eps_list[1]))
            f.write('|' + '-' * 21 + '|\n')
            f.write("\n")

    def Start(self):
        try:
            os.remove("result.txt")
        except OSError:
            pass
        links = self.get_links()
        for link in links:
            data = self.getReportText(link['link'])
            print(link)
            eps = self.getEPS(data)[:2]
            if self.EPSValid(eps):
                name = self.getName(data)
                ticker = link['ticker']
                link = link['link']
                self.WriteToFile(name, ticker, eps)

if __name__ == "__main__":
    main = Main()
    main.Start()
