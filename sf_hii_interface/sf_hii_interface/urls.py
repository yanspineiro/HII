import debug_toolbar
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^sf_bridge/', include('sf_bridge.urls')),
                       url(r'^api-auth/', include('rest_framework.urls'), name='rest_framework'),
                       url(r'^__debug__/', include(debug_toolbar.urls)),

                       )
