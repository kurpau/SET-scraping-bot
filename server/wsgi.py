from app import create_app
from waitress import serve
import webbrowser
from threading import Timer

app = create_app()


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    Timer(1, open_browser).start()  # Open a web browser window.
    serve(app, host="0.0.0.0", port=5000)
