import logging

from django.conf import settings 
from django.db import transaction

from tardis.tardis_portal.models import ExperimentParameterSet, Schema, ParameterName, ExperimentParameter

uri_namespace = settings.RELATED_URI_SCHEMA_NAMESPACE
publication_namespace = settings.RELATED_PUBLICATION_SCHEMA_NAMESPACE

uri_uri_name = 'uri'
uri_title_name = 'title'
uri_notes_name = 'notes'

pub_url_name = 'url'
pub_title_name = 'title'
pub_notes_name = 'notes'

logger = logging.getLogger(__name__)

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
           'url': x.experimentparameter_set.get(name=self.pub_url_name),
           'title': x.experimentparameter_set.get(name=self.pub_title_name),
           'notes': _get_or_none(x.experimentparameter_set, name=self.pub_notes_name),  # notes is optional
           'id': x.id
        } for x in paramsets]
        return dicts

    @transaction.commit_on_success
    def add_uri(self, cleaned_data):
        logger.debug('adding uri')
        logger.debug(cleaned_data)

        notes = cleaned_data['notes']
        uri = cleaned_data['uri']
        title = cleaned_data['title']

        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.uri_schema)
        eps.save()

        ExperimentParameter(parameterset=eps, name=self.uri_uri_name, string_value=uri).save()
        ExperimentParameter(parameterset=eps, name=self.uri_notes_name, string_value=notes).save()
        ExperimentParameter(parameterset=eps, name=self.uri_title_name, string_value=title).save()

    @transaction.commit_on_success
    def add_publication(self, cleaned_data):
        logger.debug('adding publication')
        logger.debug(cleaned_data)

        notes = cleaned_data['notes']
        url = cleaned_data['url']
        title = cleaned_data['title']

        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.publication_schema)
        eps.save()

        ExperimentParameter(parameterset=eps, name=self.pub_url_name, string_value=url).save()
        ExperimentParameter(parameterset=eps, name=self.pub_notes_name, string_value=notes).save()
        ExperimentParameter(parameterset=eps, name=self.pub_title_name, string_value=title).save()



    @transaction.commit_on_success
    def edit_uri(self, cleaned_data, parameterset_id):
        logger.debug('editing uri %s' % parameterset_id)
        logger.debug(cleaned_data)

        notes = cleaned_data['notes']
        uri = cleaned_data['uri']
        title = cleaned_data['title']

        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.uri_schema, pk=parameterset_id)

        _update(eps, self.uri_notes_name, notes)
        _update(eps, self.uri_title_name, title)
        _update(eps, self.uri_uri_name, uri)

    @transaction.commit_on_success
    def edit_publication(self, cleaned_data, parameterset_id):
        logger.debug('editing publication %s' % parameterset_id)
        logger.debug(cleaned_data)

        notes = cleaned_data['notes']
        url = cleaned_data['url']
        title = cleaned_data['title']

        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.publication_schema, pk=parameterset_id)

        _update(eps, self.pub_notes_name, notes)
        _update(eps, self.pub_title_name, title)
        _update(eps, self.pub_url_name, url)

    def delete_uri(self, parameterset_id):
        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.uri_schema, pk=parameterset_id)
        eps.delete()

    def delete_publication(self, parameterset_id):
        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.publication_schema, pk=parameterset_id)
        eps.delete()

    def uri_form_data(self, parameterset_id):
        data = {}
        eps = ExperimentParameterSet.objects.get(pk=parameterset_id, schema=self.uri_schema)
        data['uri'] = ExperimentParameter.objects.get(parameterset=eps, name=self.uri_uri_name).string_value
        data['notes'] = ExperimentParameter.objects.get(parameterset=eps, name=self.uri_notes_name).string_value
        data['title'] = ExperimentParameter.objects.get(parameterset=eps, name=self.uri_title_name).string_value
        return data

    def publication_form_data(self, parameterset_id):
        data = {}
        eps = ExperimentParameterSet.objects.get(pk=parameterset_id, schema=self.publication_schema)
        data['url'] = ExperimentParameter.objects.get(parameterset=eps, name=self.pub_url_name).string_value
        data['notes'] = ExperimentParameter.objects.get(parameterset=eps, name=self.pub_notes_name).string_value
        data['title'] = ExperimentParameter.objects.get(parameterset=eps, name=self.pub_title_name).string_value
        return data
        

def _update(parameterset, name, string_value):
    param = ExperimentParameter.objects.get(parameterset=parameterset, name=name)
    param.string_value = string_value
    param.save()

def _get_or_none(queryset, **kwargs):
    objs = queryset.filter(**kwargs)
    if len(objs) != 1:
        return None
    else:
        return objs[0]
