from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'account.views.index', name='home'),
    url(r'^(?P<account_id>\d+)/$', 'account.views.detail'),

    # url(r'^SocialExpressApp/', include('SocialExpressApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^account/$', 'account.views.index'),
    url(r'^account/(?P<account_id>\d+)/$', 'account.views.detail'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls'))
)
