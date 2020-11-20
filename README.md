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