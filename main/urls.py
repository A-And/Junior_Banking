from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', 'login.views.landing', name='landing'),
                       url(r'^admin/', include(admin.site.urls)),
)
