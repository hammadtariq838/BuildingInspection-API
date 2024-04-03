# Building Inspection - API

## First Time Setup
```bash
  virtualenv venv
  pip install -r requirements.txt
  python manage.py migrate
```
### Create Super User
```bash
  python manage.py createsuperuser
```
## Running the server
```bash
  python manage.py runserver
```
## Check & Create Migrations
```bash
  python manage.py makemigrations
  python manage.py migrate
```
