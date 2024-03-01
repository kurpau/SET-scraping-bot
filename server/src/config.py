import logging
import os
import sys


def setup_logging():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    log_level = logging.DEBUG
    log_filename = "application.log"

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create error file handler and set level to error
    file_handler = logging.FileHandler(log_filename, mode="a")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Only error messages will be shown from playwright
    logging.getLogger("playwright").setLevel(logging.ERROR)

    # If the application is frozen (like a packaged exe), adjust the file path
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
        log_filename = os.path.join(application_path, log_filename)
        file_handler.baseFilename = log_filename
        os.chdir(application_path)
    else:
        application_path = os.path.dirname(__file__)
        log_filename = os.path.join(application_path, log_filename)
        file_handler.baseFilename = log_filename
