# playwright-web-scraping

Example repository for web scraping a single page application with Playwright.

## Setup

I wrote this example application for Python 3.10, although it should work in python versions 3.9+. It should also work in lower versions of python 3 if the type hints are removed. To get started, you can `pip install` the necessary third-party requirements `flask` and `playwright` in a virtual environment and install Playwright's browser support.

```bash
pip install --upgrade pip
pip install flask playwright # or pip install -r requirements.txt
playwright install
```

## Run script on the command line

You can run the script on the command line with the following:

```bash
python check_dancer_points.py
```

You'll be asked to input a name or dancer ID.

## Run Flask application

You can run the flask application locally with the following:

```bash
flask --app check_dancer_points run --reload
```

Then go to `localhost:5000`. Provide a dancer's name or ID in the query string. For example, you could go to <http://localhost:5000/?name_or_id=theodore%20williams> to search for my name. `%20` is the URL encoding for a space character.

## Run the tests

Tests require the `pytest` and `pytest-cov` packages, so first, run:

```bash
pip install pytest pytest-cov  # or pip install -r requirements.txt
```

Run the pytests with:

```bash
pytest .
```

Run the pytests with coverage:

```bash
pytest --cov --cov-report=html .
```
