from flask import jsonify, request, send_from_directory
from src.scraper import Scraper
from src.stock_service import StockService
from src.config import setup_logging
import logging

setup_logging()

scraper = Scraper()
stock_service = StockService(scraper)


def init_routes(app):
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

    @app.route("/")
    def serve_frontend():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        if path != "" and (
            path.endswith(".js") or path.endswith(".css") or path.endswith(".ico")
        ):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")
