import logging


def get_eps_limit():
    while True:
        user_input = input("Enter the EPS limit (Default is 0.02): ")
        if user_input == "":
            return 0.02
        try:
            return float(user_input)
        except ValueError:
            logging.info(
                "Please enter a valid number for EPS limit or press Enter for default."
            )
