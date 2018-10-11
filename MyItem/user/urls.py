from django.conf.urls import include, url
from django.contrib import admin
from user import views

urlpatterns = [
    url(r'^register$', views.RegisterView.as_view(), name='register'),

    url(r'^login$', views.login, name='login'),
]
