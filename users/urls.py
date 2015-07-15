from __future__ import unicode_literals

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^set-password/$', views.SetPasswordView.as_view(), name='set_password'),
    url(r'^check-your-email/$', views.ValidationSentView.as_view(), name='validation_sent'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    # url(r'^$', views.UserListView.as_view(),
    #     name='users'),
    #
    # url(r'^(?P<pk>\d+)/$',
    #     views.UserDetailView.as_view(),
    #     name='user'),

]

