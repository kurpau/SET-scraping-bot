from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder="dist")  # Adjust static folder path.
    CORS(app, resources={r"/*": {"origins": "*"}})

    from .views import init_routes

    init_routes(app)

    return app
