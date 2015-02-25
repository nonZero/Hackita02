from __future__ import unicode_literals

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',

    url(r'^users/$', views.UserListView.as_view(),
        name='users'),

    url(r'^users/(?P<pk>\d+)/$',
        views.UserDetailView.as_view(),
        name='user'),

    url(r'^users/import/$', views.ImportUsersView.as_view(),
        name='import_users'),


)
