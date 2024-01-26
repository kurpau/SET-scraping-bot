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
    response_object["stocks"] = scraper.fetch_stocks()
    return jsonify(response_object)


if __name__ == "__main__":
    app.run()
