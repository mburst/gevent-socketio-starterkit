from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='home'),
    url(r'^register/$', 'register', name='register'),
    url(r'^draft/(?P<league_id>\d+)/$', 'draft', name='draft'),
)