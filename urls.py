from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TeachingAid.views.home', name='home'),
    # url(r'^TeachingAid/', include('TeachingAid.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin interface
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'taCore.views.index'),
    url(r'^main/$', 'taCore.views.main_page'),
    
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'taCore.views.logout_page'),

    url(r'^knowledge/', include('knowledge.urls')),
)
