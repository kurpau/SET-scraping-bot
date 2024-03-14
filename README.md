# SET-scraping-bot

SET-scraping-bot is a scraping tool designed for extracting EPS values from SET's F45 reports.

## Getting Started

These instructions will guide you through the setup process to get the SET-scraping-bot up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker (for Docker-based setup)
- Python 3.8 or higher
- Node.js (for setting up the development environment)

### Installation

#### Using Docker

For a quick and straightforward setup, you can use Docker to run SET-scraping-bot without needing to manually install dependencies.

1. Pull the Docker image:

    ```sh
    docker pull kurpau/set-bot
    ```

2. Run the Docker container:

    ```sh
    docker run -p 5000:5000 kurpau/set-bot
    ```

#### Running with Python

To set up the environment manually for more control and development purposes, follow these steps:

1. Install the latest version of Python from [Python.org](https://www.python.org/downloads/).

2. Clone the repository:

    ```sh
    git clone https://github.com/kurpau/SET-scraping-bot.git
    ```

3. Navigate to the server directory and set up a virtual environment:

    ```sh
    cd SET-scraping-bot/server
    python -m venv .venv
    source .venv/bin/activate
    ```

    For Windows users, activate the virtual environment using:

    ```cmd
    .venv\Scripts\activate
    ```

4. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

5. Install Playwright and its dependencies:

    ```sh
    playwright install webkit
    playwright install-deps
    ```

6. Start the server:

    ```sh
    python wsgi.py
     ```

 After starting the server, the application can be accessed via [http://localhost:5000](http://localhost:5000) in your web browser.
  
### Setting Up the Development Environment

For developers planning to contribute or modify the tool, setting up the full development environment is recommended.

1. Follow the steps above to set up the server environment.

2. Navigate to the client directory:

    ```sh
    cd SET-scraping-bot/server
    ```

3. Install Node.js dependencies:

    ```sh
    npm install
    ```

4. Start the development server:

    ```sh
    npm run dev
    ```
