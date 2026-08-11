#!/bin/bash
# Production start for the single `app` container.
#
# Everything that must happen exactly once — migrations, static files, the
# superuser, fixtures, scheduled tasks — runs here, BEFORE supervisord starts
# gunicorn and the qcluster worker. That ordering is the point of the file: when
# these were two containers each ran `migrate` on boot and raced each other.

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    (python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL) ||
        true
fi

python manage.py scheduletasks
python manage.py load_version_fixture

exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf
