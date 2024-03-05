from flask import Flask
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    from .views import init_routes

    init_routes(app)

    return app

