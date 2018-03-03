from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.*$', views.index, name='index'),
    url(r'^match/(?P<matchid>[0-9]+)/$', views.match, name='match'),
    url(r'^domove/(?P<matchid>[0-9]+)/$', views.do_move, name='domove'),
    url(r'^undomove/(?P<matchid>[0-9]+)/$', views.undo_move, name='undomove'),
    url(r'^resume/(?P<matchid>[0-9]+)/$', views.resume, name='resume'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/(?P<matchid>[0-9]+)/$', views.settings, name='settings'),
    url(r'^delete/(?P<matchid>[0-9]+)/$', views.delete, name='delete'),
    url(r'^importmatch/$', views.import_match, name='importmatch'),
    url(r'^analyze/(?P<matchid>[0-9]+)/$', views.analyze, name='analyze'),
    url(r'^analyze/(?P<matchid>[0-9]+)/(?P<threadidx>[0-9]+)/(?P<rcount>[0-9]+)/$', views.analyze, name='analyze'),
    url(r'^replay/(?P<matchid>[0-9]+)/(?P<threadidx>[0-9]+)/(?P<rcount>[0-9]+)/$', views.replay, name='replay'),
    url(r'^addcomment/(?P<matchid>[0-9]+)/$', views.add_comment, name='addcomment'),
    url(r'^fetchcomments/$', views.fetch_comments, name='fetchcomments'),
    url(r'^fetchmatch/$', views.fetch_match, name='fetchmatch'),
]
