from __future__ import unicode_literals

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='detail'),
    url(r'^create/$', views.ProjectCreateView.as_view(), name='create'),
]

