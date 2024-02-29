import urllib.parse
from datetime import datetime
from config import setup_logging
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

from scraper import Scraper

setup_logging()
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


# Assuming a function to validate date strings exists
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class StockService:
    def __init__(self, scraper):
        self.scraper = scraper

    def fetch_stocks(self, from_date_str, to_date_str):
        if not is_valid_date(from_date_str) or not is_valid_date(to_date_str):
            raise ValueError("Invalid date format, expected YYYY-MM-DD.")
        url = self.construct_url(from_date_str, to_date_str)
        return self.scraper.fetch_stocks(url)

    def construct_url(self, from_date_str=None, to_date_str=None):
        from_date = (
            datetime.strptime(from_date_str, "%Y-%m-%d")
            if from_date_str
            else datetime.today()
        )
        to_date = (
            datetime.strptime(to_date_str, "%Y-%m-%d")
            if to_date_str
            else datetime.today()
        )

        url_params = {
            "source": "company",
            "securityType": "S",
            "type": "3",
            "keyword": "F45",
            "fromDate": from_date.strftime("%Y-%m-%d"),
            "toDate": to_date.strftime("%Y-%m-%d"),
        }
        return f"https://www.set.or.th/en/market/news-and-alert/news?{urllib.parse.urlencode(url_params)}"


# Dependency Injection
scraper = Scraper()  # Assuming Scraper class is defined elsewhere
stock_service = StockService(scraper)


@app.route("/stocks", methods=["GET"])
def fetch_stocks_endpoint():
    from_date_str = request.args.get("from")
    to_date_str = request.args.get("to")
    response_object = {"status": "success"}

    try:
        stocks = stock_service.fetch_stocks(from_date_str, to_date_str)
        response_object["stocks"] = stocks
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        response_object.update({"status": "error", "message": str(e)})
    except Exception as e:
        logging.error(f"Error fetching stocks: {e}")
        response_object.update(
            {"status": "error", "message": "An unexpected error occurred."}
        )
    return jsonify(response_object)


if __name__ == "__main__":
    app.run(debug=True)
