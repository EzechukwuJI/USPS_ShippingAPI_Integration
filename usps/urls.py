from django.conf.urls import patterns, url
from . import views



urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^usps/api/action=(?P<action>[-\w]+)$', views.do_api_request, name = 'api'),
]