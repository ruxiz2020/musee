# MUSEE: The library that indexes your text files by topics

## A simple organizer of text files

There are relatively large amount of text files collected for a specific area of interest.  This package will help:

1. Extract keywords from each individual text files;
2. Index the files by the extracted keywords;
3. Build and maintain the indexing in a centralized database;
4. Provide a UI for easy search among the documents;

The indexing can be re-build any time as text files collection get larger over time.

## demo

Setup virtualenv and install required dependencies

`````bash
virtualenv -p python3 env
source env/bin/activate
env/bin/pip install -r requirements.txt
env/bin/pip install . -U --force-reinstall --no-deps
`````

## run examples

`````bash
env/bin/python musee/keyword_extract/extractKeywords.py
`````

## demo UI

create db in local postgresql

`````bash
createdb musee
`````

Run db migration

`````bash
env/bin/python musee/frontend/manage.py db init
env/bin/python musee/frontend/manage.py db migrate
env/bin/python musee/frontend/manage.py db upgrade
`````

Run UI
`````bash
env/bin/python musee/frontend/app.py
`````
