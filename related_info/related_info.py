from tardis.tardis_portal.models import ExperimentParameterSet, Schema, ParameterName

uri_namespace = 'http://urischema.com/'
publication_namespace = 'http://publicationschema.com/'

uri_uri_name = 'uri'
uri_title_name = 'title'
uri_notes_name = 'notes'

pub_url_name = 'url'
pub_title_name = 'title'
pub_notes_name = 'notes'

class RelatedInfoHandler(object):
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
        self.uri_schema = Schema.objects.get(namespace=uri_namespace)
        self.publication_schema = Schema.objects.get(namespace=publication_namespace)

        self.uri_uri_name = ParameterName.objects.get(schema=self.uri_schema, name=uri_uri_name)
        self.uri_title_name = ParameterName.objects.get(schema=self.uri_schema, name=uri_title_name)
        self.uri_notes_name = ParameterName.objects.get(schema=self.uri_schema, name=uri_notes_name)

        self.uri_schema = Schema.objects.get(namespace=uri_namespace)
        self.publication_schema = Schema.objects.get(namespace=publication_namespace)

        self.pub_url_name = ParameterName.objects.get(schema=self.publication_schema, name=pub_url_name)
        self.pub_title_name = ParameterName.objects.get(schema=self.publication_schema, name=pub_title_name)
        self.pub_notes_name = ParameterName.objects.get(schema=self.publication_schema, name=pub_notes_name)

    def uris(self):
        paramsets = ExperimentParameterSet.objects.filter(experiment=self.experiment_id, schema=self.uri_schema)
        dicts = [{
           'uri': x.experimentparameter_set.get(name=self.uri_uri_name),
           'title': x.experimentparameter_set.get(name=self.uri_title_name),
           'notes': x.experimentparameter_set.get(name=self.uri_notes_name),
           'id': x.id
        } for x in paramsets]
        return dicts

    def publications(self):
        paramsets = ExperimentParameterSet.objects.filter(experiment=self.experiment_id, schema=self.publication_schema)
        dicts = [{
           'uri': x.experimentparameter_set.get(name=self.pub_url_name),
           'title': x.experimentparameter_set.get(name=self.pub_title_name),
           'notes': _get_or_none(x.experimentparameter_set, name=self.pub_notes_name),  # notes is optional
           'id': x.id
        } for x in paramsets]
        return dicts

def _get_or_none(queryset, **kwargs):
    objs = queryset.filter(**kwargs)
    if len(objs) != 1:
        return None
    else:
        return objs[0]
