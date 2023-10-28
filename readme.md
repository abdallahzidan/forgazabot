# Overview
Telegram bot targets consumer boycotts and convinces retailers across the world to stop selling products from companies profiting from Israel’s crimes. Many Israeli exporters complain that it is getting harder for them to export their products.

# 🚀 Getting Started

## Running on Local Machine

-   install dependencies using [Poetry](https://python-poetry.org "python package manager")
    ```bash
    poetry install
    ```
-   configure environment variables in `.env` file
    ```bash
    cp .env.sample .env
    ```
-   start bot in virtual environment
    ```bash
    poetry run python -m bot
    ```

## Launch in Docker

-   configure environment variables in `.env` file
    ```bash
    cp .env.sample .env
    ```
-   start virtual environment
    ```bash
    poetry shell
    ```
-   building the docker image
    ```bash
    docker-compose -f docker/docker-compose.yaml build
    ```
-   start service
    ```bash
    docker-compose -f docker/docker-compose.yaml up -d
    ```

# 🌍 Environment variables

|      variables       | description                         |
|:--------------------:|-------------------------------------|
|     `BOT_TOKEN`      | Telegram bot API token              |
|      `BOT_NAME`      | Telegram bot name                   |
|      `API_KEY`       | the name of the PostgreSQL database |
|  `SEARCH_ENGINE_ID`  | password used to authenticate       |

# 🔧 Tech Stack

-   `poetry` — development workflow
-   `docker` — to automate deployment
