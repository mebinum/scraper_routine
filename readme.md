
# Dependencies

- Python 3.11.5
- [PhantomJS Browser](https://phantomjs.org/download.html)
     * alternatively chrome or firefox can be used
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/engine/install/)

Install the dependencies

## Configure env vars

```sh
cp .env.example .env
```

Update the .env file with your own values if you are using a local postgres db

## Setup the database if using docker

```sh
# create a folder for local docker volume
mkdir -p .local/docker/data

# create temp folder used for downloading and unzipping
mkdir -p .local/temp
```

### Start the Database

```sh
# start database
docker-compose up db -d
```

## Setup Python Env

```sh
# create scraper virtual env
pyenv virtualenv 3.11.5 scraper
```

## Start project dependencies.

Run `pip install poetry` if you need to install poetry.

```sh
# select pyenv
pyenv activate scraper
poetry install
```

## Run the project

```sh
poetry run run
```
