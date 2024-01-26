from flask import Flask, jsonify
import urllib.parse
from scraper import Scraper
from datetime import datetime


app = Flask(__name__)


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
    return f"https://www.set.or.th/en/market/news-and-alert/news?{urllib.parse.urlencode(url_params)}"


def EPSValid(self, eps_list):
    curr_eps = eps_list[0]
    prev_eps = eps_list[1]
    if curr_eps > 0 and prev_eps > 0 and (curr_eps - prev_eps >= self.limit):
        return True
    return False


# Hardcoded date range
from_date = datetime(2024, 1, 1)
to_date = datetime(2024, 1, 25)  # December 31, 2023

# Call the function with hardcoded dates
url = construct_url(from_date, to_date)

# Assuming Scraper and other necessary classes and methods are defined elsewhere
scraper = Scraper(url, 0.02)
# other necessary initializations


@app.route("/stocks", methods=["GET"])
def fetch_stocks():
    response_object = {"status": "success"}
    all_stocks = scraper.fetch_stocks()

    for stock in all_stocks:
        stock_name = stock.get("stock_name")
        eps = stock.get("eps")

        if not stock_name or not eps:
            continue

        if EPSValid(eps):
            stock["valid"] = True

    response_object["stocks"] = all_stocks
    return jsonify(response_object)


if __name__ == "__main__":
    app.run(debug=True)
