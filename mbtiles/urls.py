
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^tiles/(?P<tileZoom>[0-9]+)/(?P<tileColumn>[0-9]+)/(?P<tileRow>[0-9]+).vector.pbf$', views.tiles, name='tiles'),
]
