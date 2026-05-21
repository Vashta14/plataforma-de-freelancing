#!/bin/sh
set -e

# Apply database migrations
python manage.py migrate --noinput

# Collect static files (optional)
# python manage.py collectstatic --noinput

exec "$@"
