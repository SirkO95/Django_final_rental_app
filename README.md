# Rental Home

Rental Home is a web application for renting apartments and houses in Germany.

The project was developed using Django as the backend framework and Bootstrap for the frontend.

## Features

- User registration and authentication
- Landlord and tenant roles
- Create, edit and delete property listings
- Upload listing images
- Property search
- Filtering by:
  - city
  - price
  - rooms
  - housing type
- Sorting by:
  - newest
  - oldest
  - price
  - popularity
- Booking system
- Booking confirmation and cancellation
- Reviews and ratings
- Dashboard for landlords and tenants
- View history
- Search history
- Popular listings

## Technologies

- Python 3
- Django
- SQLite
- Bootstrap 5
- HTML
- CSS
- JavaScript
- Git
- GitHub

## Project Structure

```
rental_backend/
listings/
templates/
static/
media/
manage.py
```

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rental-home.git
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

Windows

```bash
.venv\Scripts\activate
```

macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Run server

```bash
python manage.py runserver
```

Open in browser

```
http://127.0.0.1:8000/
```

## Author

Oleksandr Zakharchuk

Student project