# to deploy 

1. change the debug variable in KFSA/settings.py to False
2. change the SECRET variable in setting.py 
3. enter the pip environment with `pipenv shell`
4. run `python manage.py migrate`
5. run `python manage.py loaddata programs`
6. run `python manage.py loaddata users`
7. deploying django is done by starting the django server using gunicorn and then sitting it behind a webserver like Nginx. https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04
