from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^trips/new$', views.create_new_trip),
    url(r'^trips/edit/(?P<id>\d+)$', views.edit_trip),
    url(r'^trips/(?P<id>\d+)$', views.view_trip),
    url(r'^add_trip$', views.add_trip),
    url(r'^join/(?P<id>\d+)$', views.join_trip),
    url(r'^Remove/(?P<id>\d+)$', views.remove_trip),
    url(r'^update_trip/(?P<id>\d+)$', views.update_trip),
    url(r'^Cancel/(?P<id>\d+)$', views.cancel_trip),
]