# Job Apps Tracker

A Django web application to manage and track daily customer requests ("apps") with MongoDB backend.

## Features
- Upload Excel sheets to import apps.
- Track stages: Passed, Wayleave, In Design, USP, Remarks.
- Each stage is dated and imported from Excel.
- Passed apps are automatically deleted from the database.
- All-in-one-page dashboard for easy follow-up.

## Stack
- Django
- MongoDB (via mongoengine)
- pandas, openpyxl (for Excel import)

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Set up MongoDB and configure connection in `settings.py`.
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## To Do
- Build the main dashboard and Excel upload functionality.
- Add authentication (future).
# RajabWeb
