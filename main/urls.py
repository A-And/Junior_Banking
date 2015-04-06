from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', 'login.views.landing', name='landing'),
                       url(r'^account/(?P<user_id>[\w]+)/$', 'login.views.account', name='account'),
                       url(r'^admin/', include(admin.site.urls)),


)
