

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from openaccess import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cmsopendata.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^TermsofUse$',
        TemplateView.as_view(template_name="openaccess/termsofuse.html"),
        name='termsofuse'),
    url(r'^PrivacyPolicy$',
        TemplateView.as_view(template_name="openaccess/privacypolicy.html"),
        name='privacypolicy'),
    url(r'^Contact$', 
        TemplateView.as_view(template_name="openaccess/contact.html"),
        name='contact'),
    url(r'^Analysis$', views.AnalysisView.as_view(), name='analysis'),
)
