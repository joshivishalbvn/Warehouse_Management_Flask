#!/bin/bash

# Start Celery worker in the background
celery -A wsgi.celery worker --loglevel=info &


# Start Celery Beat scheduler
celery -A wsgi.celery beat --loglevel=info  



