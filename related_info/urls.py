from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    'tardis.apps.related_info.views',
    (r'^(?P<experiment_id>\d+)/$', 'index'),
    (r'^(?P<experiment_id>\d+)/add_info/$', 'add_info'),
    (r'^(?P<experiment_id>\d+)/delete_info/(?P<parameterset_id>\d+)/$', 'delete_info'),
    (r'^(?P<experiment_id>\d+)/edit_info/(?P<parameterset_id>\d+)/$', 'edit_info'),
    )
