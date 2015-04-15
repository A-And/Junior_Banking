from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', 'login.views.landing', name='landing'),
                       url(r'^home/$', 'login.views.home', name='home'),
                       url(r'^account/$', 'login.views.account', name='account'),
                       url(r'^goals/$', 'login.views.goals', name='goals'),
                       url(r'^guide/$', 'login.views.guide', name='guide'),
                       url(r'^profile/$', 'login.views.profile', name='profile'),
                       url(r'^admin/', include(admin.site.urls)),


)
# Default 404 override
handler404 = 'login.views.http404'
