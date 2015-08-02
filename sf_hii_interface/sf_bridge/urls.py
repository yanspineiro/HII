from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('sf_bridge',
                       url(r'^api/$', 'views.sf_bridge_list', name='views.sf_bridge_list'),
                       url(r'^api/(?P<pk>[0-9]+)$', 'views.sf_bridge_detail', name='views.sf_bridge_detail'),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)