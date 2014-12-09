from django.conf.urls import patterns, include, url
from django.contrib import admin

from cmsopendata import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cmsopendata.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('openaccess.urls', namespace="openaccess")),
)

