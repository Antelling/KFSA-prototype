# Kutztown Faculty Support Application

Ignore the prototype in the name.

### Features Implemented So Far:

- create an account 
- select other existing accounts as students you advise (this is bad, will be changed later)
- choose a checksheet for students, if they don't already have one (also bad and will be changed)
- view all advisement records for a student (students can have numerous advisors)
- edit an existing advisment record (should this be allowed? )
- create a new advisement record, filled in with the most recent record's data
- view an old advisement record


### environment setup
First, install pipenv for whatever operating system you are using. 
Then, clone the repo with git and then run `pipenv install` to install the pip environment. 
Then `pipenv shell` to enter the shell. 
Then type `python manage.py runserver` to start the development server. 

You probably also want to create a superuser account. Go through 
https://docs.djangoproject.com/en/3.1/intro/tutorial01/ if you've never used django. 

I highly recommend going through https://www.jetbrains.com/shop/eform/students to get free Pycharm Professional 
which is a great IDE for django with built in debugger and VCS and error highlighting. 

## To Do:

A selection of tasks that can be completed given the current state of the project. 

- make all the template html files extend base.html
- add a CSS framework to base.html (hopefully bootstrap)
- modify all templates to be pretty with the CSS framework
- add a favicon 
- fix any of the FIXME comments in the code 
- create JSON files for all the programs offered by the CSC department and put them in advisment/checksheet_templates


## Longterm To Do: 

tasks which are a lot of work and probably need discussion 

- create student records instead of using existing accounts

- create account permissions for
    - editing checksheet templates
    - creating students and assigning advisors 
    - advising students (this should just be the default account)
  
- actually implement security. Right now manually editing the URL lets you edit any records. 
