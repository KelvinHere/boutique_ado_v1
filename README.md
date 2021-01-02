# E-commerce site

## Quick Django setup
- `$ pip3 install django`
- `$ django-admin startproject project_name_here .`
- `$ python3 manage.py runserver` check django is working
- `$ python3 manage.py migrate` migrate all the tables of your installed apps to create your database file.
- `$ python3 manage.py createsuperuser` create project admin

## Quick Allauth setup

* `$ pip install django-allauth` Open source login system
* [Allauth link for setup in settings.py](https://django-allauth.readthedocs.io/en/latest/installation.html)
* In settings.py TEMPLATES the line `'django.template.context_processors.request'` is required by allauth

- Add AUTHENTICATION_BACKENDS list to settings.py
- Add `site_id = 1` under AUTHENTICATION_BACKENDS
- Add the following to installed apps
    - 'django.contrib.sites',
    - 'allauth',
    - 'allauth.account',
    - 'allauth.socialaccount',

* Add in urls.py URL_PATTERNS `path('accounts', include('allauth.urls')),`
* Urls for login, logout, password reset etc

- migrate again as we have new apps installed

- You should now be able to login as admin

### Social media login note
In sites > Domain Name > example_whatever change this to something appropriate as some social logins require this info

### Allauth TEMPLATES
- These live in site packages, make a route templates/allauth dir
- drop in the templates ie:-
- `cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates/allauth/`
- customise

### FREE SAMPLE DATA SETS
Caggle.com

### Fixtures
Fixtures (a dir called fixtures in an app) are used to load data quickly into a django database so not to have to do it manually in admin

### Migrations

* Create models
* `python3 manage.py makemigrations --dry-run` Check migrations with dry run for errors
* `python3 manage.py makemigrations` To make migrations
* `python3 manage.py migrate --plan` To plan the excution of migrations to make sure we are not missing anything
* `python3 manage.py migrate` Run the migrations

### CrispyForms forms
- `pip3 install django-crispy-forms` allows bootstrap style formating of forms automatically
- In settings.py
    - add `'crispy_forms',` to INSTALLED_APPS
    - tell it what pack by adding `CRISPY_TEMPLATE_PACK = 'bootstrap4'`
    - add builtins to allow sitewide use of these `'builtins' : ['crispy_forms.templatetags.crispy_forms_tags', 'crispy_forms.templatetags.crispy_forms_field',]` check the file for location of this (inside templates)
- Remember to freeze requirements

### Django Countries
* List of countries with ISO codes
* `pip3 install django-countries`
* pip freeze
* For drop down menu of countries that converts to ISO code in form

### Stripe
`pip3 install stripe`

### Heroku & PostgresDB

- Create app
- On heroku website > resources > search postgres > free hobby tier
- install dj-database `pip3 install dj_database_url`
- install psycopg2-binary `pip3 install psycopg2-binary`
- freeze requirements `pip3 freeze > requirements.txt`

- Set up PostgresDB
- comment out database from settings.py
- add `DATABASES = {'default': dj_database_url.parse('POSTGRES_ENV_VAR_FROM_HEROKU_SETTINGS')}` instead
- show migrations will show you the DB needs to be migrated again
    - `python3 manage.py migrate`
- Use fixtures to move items to the new database
    - `python3 manage.py loaddata categories`
    - `python3 manage.py loaddata products`
    - Do categories first as products depend on the categories
    - `python3 manage.py createsuperuser` and complete fields

- IMPORTANT
- remove `DATABASES = {'default': dj_database_url.parse('POSTGRES_ENV_VAR_FROM_HEROKU_SETTINGS')}`
- uncomment original DATABASES in settings.py
- So the DB env_var does not end up in version control

- Now the heroku app and database are ready to go