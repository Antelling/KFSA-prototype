# to deploy 

1. change the debug variable in KFSA/settings.py to False
2. change the SECRET variable in setting.py 
3. enter the pip environment with `pipenv shell`
4. run `python manage.py migrate`
5. run `python manage.py loaddata programs`
6. run `python manage.py loaddata users`
7. run `python manage.py runserver`
8. deploying django is done by starting the django server using gunicorn and then sitting it behind a webserver like Nginx. https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04


# integrating authentication

Authentication is handled by django, so asking it to use a particular authentication protocol appears to be quite simple.  https://github.com/fangli/django-saml2-auth 

# choosing the database 

Changing what database django uses only requires editing the database settings object in KFSA/setting.py https://docs.djangoproject.com/en/3.2/topics/db/multi-db/
