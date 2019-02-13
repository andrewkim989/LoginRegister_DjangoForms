from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.registerUser),
    url(r'^login$', views.loginUser),
	url(r'^home$', views.home),
	url(r'^logout$', views.logout)
]