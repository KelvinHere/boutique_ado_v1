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

### Gunicorn

- Install a webserver, we will use
- `pip3 install gunicorn`
- freeze requirements

### Procfile

- Create procfile to tell heroku how to run app (tell heroku to run a web dyno)


### Deploy to heroku

- login to CLI
- Temp stop heroku from collecting static files when we deploy
    - `heroku config:set DISABLE_COLLECTSTATIC=1 --app boutique-ado-kelvinhere`
- Add hostname of the heroku app to "ALLOWED_HOSTS" in settings.py

- initialise heoku git `heroku git:remote -a boutique-ado-kelvinhere`
- push to heroku `git push heroku master`
- Link to github auto deploy if you want

- Goto a django secret key generator and generate a key, add this to heroku > config vars as SECRET_KEY

### AMAZON WEB SERVICES s3

- Cloud based storage service (for this project to store images)
- aws.amazon.com and create or login to your aws account
- My account > aws management console
- Services > s3
- Open s3 and create a bucket (place to store files) name this appropriatley (same as hheroku app) and select region closest to you
- Uncheck block all public access, check the warning

* #### Open bucket
- Properties: static website hosting > Use this bucket to host a website
    - Fill in default values (index document: index.html) (they wont be used in our case)
    - Save

- Permissions: 
    - CORS configuration: Sets up the required access between our Heroku app and this s3 bucket.
    - Cors config `[{"AllowedHeaders": ["Authorization"], "AllowedMethods": ["GET"], "AllowedOrigins": ["*"], "ExposeHeaders": []}]`

    - Bucket Policy > Generate policy > 
        - typeofpolicy:s3bucketpolicy
        - principal:*
        - actions:getobject
        - copy ARN from bucket policy into ARN in policy maker
        - click add statement then generate policy
        - then copy the generated policy into the bucket policy editor
        - add /* to the end of the resource key so all resources can be used

    - Access control list:
        - Everyone (public access) check "list"
        - This will allow full public access

* #### Create a user to access the bucket
    - AWS services > IAM
    - create a group for the user to live in
        - Groups > create group and name it (manage-boutique-ado-kelvinhere)
        - Create group (without attaching policy)
    - create an access policy to give the group access to the s3 bucket
        - Policy > create policy
        - Json > import managed policy > search s3
        - import `AmazonS3FullAccess` policy (Do not leave like this)
        - Get the bucket ARN from the s3 bucket and place it in `"Resources"` like below
        - `"Resource": ["arn:aws:s3:::boutique-ado-kelvinhere", "arn:aws:s3:::boutique-ado-kelvinhere/*"]`
        - This will create one rule for the bucker 1st in list and one rule for all the files/folders in bucket (/*)
        - Click review policy and give it name and desc then create policy
        - Go back to groups and attach the newly created policy to the group
    - Create a user so it can use the policy in the group to access the files
        - Users > add user
        - Create a user (boutique-ado-static-files-user)
        - give them programatic access
        - select next
        - add user to group > check the group we created
        - click next to the end and select create user
        - download the CSV which will contain the user and SECRET_ACCESS key to allow s3 authentication through the django app (do not leak these)
        - you must download these immediatley as you cannot download again once we are off the page

* #### Configure Django to connect to s3

- `pip3 install boto3`
- `pip3 install django-storages`
- Freeze
- Add `'storages',` to installed apps in settings.py
- Check diff for settings.py to see the setup for AWS in the commit "FEAT: Added AWS to project and locations for static files"