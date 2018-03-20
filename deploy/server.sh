#!/bin/sh

gunicorn --access-logfile - --error-logfile - -b 0.0.0.0:8000 infopankki.wsgi
