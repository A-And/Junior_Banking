from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', 'login.views.landing', name='landing'),
                       url(r'^home/(?P<user_id>[\w]+)/$', 'login.views.home', name='home'),
                       url(r'^account/(?P<user_id>[\w]+)/$', 'login.views.account', name='account'),
                       url(r'^goals/(?P<user_id>[\w]+)/$', 'login.views.goals', name='goals'),
                       url(r'^guide/(?P<user_id>[\w]+)/$', 'login.views.guide', name='guide'),
                       url(r'^admin/', include(admin.site.urls)),


)
# Default 404 override
handler404 = 'login.views.http404'
