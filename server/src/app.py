from flask import Flask, jsonify, request
import urllib.parse
from scraper import Scraper
from datetime import datetime


app = Flask(__name__)


def construct_url(from_date_str=None, to_date_str=None):
    from_date = (
        datetime.strptime(from_date_str, "%Y-%m-%d")
        if from_date_str
        else datetime.today()
    )
    to_date = (
        datetime.strptime(to_date_str, "%Y-%m-%d") if to_date_str else datetime.today()
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


@app.route("/stocks", methods=["GET"])
def fetch_stocks():
    from_date_str = request.args.get("from")
    to_date_str = request.args.get("to")

    url = construct_url(from_date_str, to_date_str)

    scraper = Scraper()
    response_object = {"status": "success"}
    response_object["stocks"] = scraper.fetch_stocks(url)
    return jsonify(response_object)


if __name__ == "__main__":
    app.run()
