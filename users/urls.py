from __future__ import unicode_literals

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # url(r'^$', views.UserListView.as_view(),
    #     name='users'),
    #
    # url(r'^(?P<pk>\d+)/$',
    #     views.UserDetailView.as_view(),
    #     name='user'),

]

