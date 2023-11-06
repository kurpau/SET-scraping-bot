# SET-scraping-bot

SET-scraping-bot is a custom scraping tool designed for extracting EPS values from SET's F45 reports.

## Table of Contents

- [Installation](#installation)
- [Standalone Executable](#standalone-executable)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Usage](#usage)
  - [Using the Standalone Executable](#using-the-standalone-executable)
  - [Running from Source](#running-from-source)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Installation

This section covers the setup process for running the bot either directly using the executable or by setting up a development environment to run the source code.

### Standalone Executable

To run the bot without any setup:

1. Navigate to the [Releases](https://github.com/kurpau/SET-scraping-bot/releases) page.
2. Download the `SETbot.exe` (Currently works only on Windows)
3. Run the file to start the bot.

### Setting Up the Development Environment

If you need to run the bot from the source code or wish to modify the code, follow these steps:

- Install the latest version of Python from [Python.org](https://www.python.org/downloads/).
- Clone the repository:

  ```sh
  git clone https://github.com/kurpau/SET-scraping-bot.git
  ```

- Navigate to the directory and install dependencies:

  ```sh
  cd SET-scraping-bot
  pip install -r requirements.txt
  ```

## Usage

### Using the Standalone Executable

Run `SET-scraping-bot.exe` to start the bot. If command-line arguments are necessary, execute the following in the command prompt or terminal:

```sh
./SET-scraping-bot.exe [arguments]
```

### Running from Source

To execute the bot from the Python script:

1. Open a terminal or command prompt in the project directory.
2. Run the script with:
   ```sh
   python main.py
   ```
