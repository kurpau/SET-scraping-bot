from flask import Flask
from flask_cors import CORS
import os


def create_app():
    client_dist_dir = os.path.abspath("client/dist/")

    app = Flask(__name__, static_folder=client_dist_dir)
    print(app.static_folder)
    CORS(app, resources={r"/*": {"origins": "*"}})

    from .views import init_routes

    init_routes(app)

    return app

