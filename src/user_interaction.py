import logging
import os

def get_eps_limit():
    while True:
        user_input = input("Enter the EPS limit (Default is 0.02): ")
        if user_input == '':
            return 0.02
        try:
            return float(user_input)
        except ValueError:
            logging.info("Please enter a valid number for EPS limit or press Enter for default.")

def clear_cache_if_requested():
    while True:  # Start a loop that will continue until it breaks
        clear_cache = input("Would you like to erase cached data? [y]es/[n]o (Default is 'no'): ").lower().strip()
        if clear_cache == "y":
            cache_path = os.path.join(os.getcwd(), "cache.txt")
            if os.path.exists(cache_path):
                os.remove(cache_path)
                logging.info("Cache cleared!")
            else:
                logging.info("No cache to clear.")
            break  # Break the loop after the cache is cleared
        elif clear_cache == "n" or clear_cache == "":
            logging.info("Using values stored in cache!")
            break  # Break the loop if the user doesn't want to clear the cache
        else:
            # Warn the user and continue the loop, prompting again
            logging.warning("Invalid input. Please enter 'y' to clear cache, 'n' to continue with the existing cache, or simply press Enter for default ('no').")
