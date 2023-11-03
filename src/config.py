import logging
import sys
import os

# Basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Only error messages will be shown from pyppeteer
logging.getLogger("pyppeteer").setLevel(logging.ERROR)

# If the application is frozen (like a packaged exe), change the directory to the executable's directory
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    application_path = os.path.dirname(__file__)

output_dir = os.getcwd()
