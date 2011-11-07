from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    'tardis.apps.related_info.views',
    (r'^(?P<experiment_id>\d+)/$', 'index'),
    (r'^(?P<experiment_id>\d+)/add_uri/$', 'add_uri'),
    (r'^(?P<experiment_id>\d+)/add_publication/$', 'add_publication'),
    (r'^(?P<experiment_id>\d+)/delete_uri/(?P<parameterset_id>\d+)/$', 'delete_uri'),
    (r'^(?P<experiment_id>\d+)/delete_publication/(?P<parameterset_id>\d+)/$', 'delete_publication'),
    (r'^(?P<experiment_id>\d+)/edit_uri/(?P<parameterset_id>\d+)/$', 'edit_uri'),
    (r'^(?P<experiment_id>\d+)/edit_publication/(?P<parameterset_id>\d+)/$', 'edit_publication'),
    )
