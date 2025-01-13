from app import create_app
import webbrowser
import os

app = create_app()

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == "__main__":
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        open_browser()
    app.run(host="0.0.0.0", debug=False, port=5000)