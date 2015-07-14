from django.conf.urls import include, url
from django.contrib import admin

from website import views

i = lambda s, prefix=None: url(r'^{}/'.format(prefix or s),
                               include('{}.urls'.format(s),
                                       namespace=prefix or s))

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^program$', views.ProgramView.as_view(), name='program'),
    url(r'^faq$', views.FAQView.as_view(), name='faq'),
    # url(r'^$', views.CreateProjectView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),
    i("projects"),
    i("users"),
    i("student_applications", "sa"),

    url(r'^admin/', include(admin.site.urls)),
]
