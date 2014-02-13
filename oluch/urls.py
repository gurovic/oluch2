from django.conf.urls import patterns, include, url
from oluch import settings
from django.contrib.auth import login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register$', 'oluch.views.register', name='register'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'oluch.views.logout_user', name='logout'),
    url(r'^contest_list$', 'oluch.views.contest_list', name='contest_list'),

    url(r'^user/(\d+)$', 'oluch.views.user', name='user'),

    url(r'^jury/(\d+)$', 'oluch.views.jury', name='jury'),
    url(r'^jury_list$', 'oluch.views.jury_list', name='jury_list'),
    url(r'^check/(?P<contest_id>\d+)/(?P<time>[123])../(?P<problem_id>\d+)$', 'oluch.views.check', name='check'),
    url(r'^check/(?P<contest_id>\d+)/(?P<time>[123])../(?P<problem_id>\d+)/(?P<submit_id>\d+)$', 'oluch.views.check', name='check'), 
    url(r'^solution_stat/(?P<contest_id>\d+)	$', 'oluch.views.solution_stat', name='solution_stat'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^results/(?P<contest_id>\d+)$', 'oluch.views.results', name='results'),

    # OLD
    url(r'^clear$', 'oluch.views.clear_minus_one', name='clear'),
    # url(r'^statistics$', 'oluch.views.statistics', name='statistics'),
    # url(r'^statistics/(P?<submit>.+)$', 'oluch.views.statistics', name='statistics'),
    url(r'^source/(?P<submit_id>.+)$', 'oluch.views.source', name='source'),
    url(r'^source$', 'oluch.views.source', {'submit_id':0}, name='source'),
    url(r'^rate/(?P<contest_id>\d+)/(?P<submit_id>\d+)/(?P<time>[123])$', 'oluch.views.rate', name='rate'),


)
