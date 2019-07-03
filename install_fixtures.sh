#!/bin/bash
# source ../virtualenv/bin/activate
# ../virtualenv/bin/python manage.py reset_db
# ../virtualenv/bin/python manage.py makemigrations
# ../virtualenv/bin/python manage.py migrate
../virtualenv/bin/python manage.py loaddata districts.json
../virtualenv/bin/python manage.py loaddata vdcs.json
../virtualenv/bin/python manage.py loaddata parties.json
../virtualenv/bin/python manage.py loaddata organisations.json
../virtualenv/bin/python manage.py loaddata morbidities.json
../virtualenv/bin/python manage.py loaddata icds.json
../virtualenv/bin/python manage.py loaddata outreaches.json
../virtualenv/bin/python manage.py loaddata groups.json
../virtualenv/bin/python manage.py createsuperuser
