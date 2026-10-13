# URL Shortener
A Python Flask web application that converts long URLs into short links and redirects visitors to the original destination.

## Features
- HTTP/HTTPS URL validation
- Six-character unique short codes
- SQLite storage through Flask-SQLAlchemy
- Redirect handling and 404 page
- Visit counter and recent URL history
- Copy-to-clipboard button

## Run locally
1. Install Python 3.10 or later.
2. Create a virtual environment: `py -m venv .venv`
3. Activate it in PowerShell: `.venv\\Scripts\\Activate.ps1`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python app.py`
6. Open `http://127.0.0.1:5000`

The SQLite database is created automatically. This is an academic prototype, not a production service. Before deployment, disable debug mode, set a strong `SECRET_KEY`, use HTTPS, and add rate limiting and abuse controls.
