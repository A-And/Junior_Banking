from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', 'login.views.landing', name='landing'),
                       url(r'^home/$', 'login.views.home', name='home'),
                       url(r'^account/$', 'login.views.account', name='account'),
                       url(r'^goals/$', 'login.views.goals', name='goals'),
                       url(r'^signup/$', 'login.views.signup', name='signup'),
                       url(r'^guide/$', 'login.views.guide', name='guide'),
                       url(r'^profile/$', 'login.views.profile', name='profile'),
                       url(r'^ATMs/$', 'login.views.ATMs', name='ATMs'),
                       url(r'^collection/$', 'login.views.collection', name='collection'),
                       url(r'^.*/?logout[/w]?$', 'login.views.logout', name = 'logout'),
                       url(r'^parent/$', 'login.views.parent', name='parent'),
                       url(r'^references/$', 'login.views.references', name='references'),
                       url(r'^admin/', include(admin.site.urls)),


)
# Default 404 override
handler404 = 'login.views.http404'
handler403 = 'login.views.http403'
