# graceful-wasp
Mbtiles server in django

Useful commands
===============

To configure nginx, uWSGI, systemd: https://gist.github.com/TimSC/0193fa92d7fe5b63769eeca5c42fd5d5

* sudo pip install django
* python manage.py migrate
* python manage.py collectstatic
* python manage.py createsuperuser

Add "add_header Access-Control-Allow-Origin *;" possibly to nginx configuration: http://serverfault.com/a/176729/375337
