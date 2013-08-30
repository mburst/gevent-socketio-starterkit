from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='home'),
    url(r'^register/$', 'register', name='register'),
    url(r'^t/(?P<username>\w+)/$', 'user_profile', name='user_profile'),
)