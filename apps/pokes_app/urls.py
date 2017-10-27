from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^pokes$', views.home),
    url(r'^addpoke/(?P<number>\d+)$', views.addpoke),
    url(r'^logout$', views.logout)
]