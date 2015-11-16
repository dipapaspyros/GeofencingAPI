"""test_api_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from location_app.geofencing_api import views
from location_app.geofencing_api.api import graphs, clients

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # home page
    url(r'^$', views.main_page),

    url(r'^api/users/$', views.get_users),
    url(r'^api/users/in-group/$', views.get_users_in_group),

    # graph api
    url(r'^api/nodes/$', graphs.graphs),
    url(r'^api/node/(?P<pk>.*)/$', graphs.graph),

    # client api
    url(r'^api/clients/$', clients.clients),
    url(r'^api/client/(?P<pk>.*)/$', clients.client),
]
