from django.conf.urls import url
from django.contrib import admin
from pals import views

app_name='pals'

urlpatterns = [
    url(r'^(?P<page>\d+)?/$', views.index, name='index'),
    url(r'^(?P<userId>\d+)/delete_user', views.delete_user, name='deleteUser'),
    url(r'^/detail/(?P<userId>\d+)/(?P<page>\d+)$', views.detail, name='detail'),

]
