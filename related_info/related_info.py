import logging

from django.conf import settings 
from django.db import transaction

from tardis.tardis_portal.models import ExperimentParameterSet, Schema, ParameterName, ExperimentParameter

namespace = settings.RELATED_INFO_SCHEMA_NAMESPACE

type_name = 'type'
identifier_type_name = 'identifier_type'
identifier_name = 'identifier'
title_name = 'title'
notes_name = 'notes'

logger = logging.getLogger(__name__)

class RelatedInfoHandler(object):
    def __init__(self, experiment_id):
        self.experiment_id = experiment_id
        self.schema = Schema.objects.get(namespace=namespace)

        self.type_name = ParameterName.objects.get(schema=self.schema, name=type_name)
        self.identifier_type_name = ParameterName.objects.get(schema=self.schema, name=identifier_type_name)
        self.identifier_name = ParameterName.objects.get(schema=self.schema, name=identifier_name)
        self.title_name = ParameterName.objects.get(schema=self.schema, name=title_name)
        self.notes_name = ParameterName.objects.get(schema=self.schema, name=notes_name)

    def info_list(self):
        paramsets = ExperimentParameterSet.objects.filter(experiment=self.experiment_id, schema=self.schema)
        dicts = []
        for paramset in paramsets:
            params = paramset.experimentparameter_set
            dicto = {
               'type': _get_or_none(params, name=self.type_name),
               'identifier_type': params.get(name=self.identifier_type_name),
               'identifier': params.get(name=self.identifier_name),
               'title': _get_or_none(params, name=self.title_name),
               'notes': _get_or_none(params, name=self.notes_name),
               'id': paramset.id
            }
            dicts.append(dicto)
        return dicts

    @transaction.commit_on_success
    def add_info(self, cleaned_data):
        logger.debug('adding info')
        logger.debug(cleaned_data)

        type = cleaned_data['type']
        identifier_type = cleaned_data['identifier_type']
        identifier = cleaned_data['identifier']
        title = cleaned_data['title']
        notes = cleaned_data['notes']

        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.schema)
        eps.save()

        _maybe_add(eps, self.type_name, type)
        _maybe_add(eps, self.identifier_type_name, identifier_type, force=True)
        _maybe_add(eps, self.identifier_name, identifier, force=True)
        _maybe_add(eps, self.title_name, title)
        _maybe_add(eps, self.notes_name, notes)

    @transaction.commit_on_success
    def edit_info(self, cleaned_data, parameterset_id):
        logger.debug('editing info %s' % parameterset_id)
        logger.debug(cleaned_data)

        type = cleaned_data['type']
        identifier_type = cleaned_data['identifier_type']
        identifier = cleaned_data['identifier']
        title = cleaned_data['title']
        notes = cleaned_data['notes']

        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.schema, pk=parameterset_id)

        _update(eps, self.type_name, type)
        _update(eps, self.identifier_type_name, identifier_type)
        _update(eps, self.identifier_name, identifier)
        _update(eps, self.title_name, title)
        _update(eps, self.notes_name, notes)


    def delete_info(self, parameterset_id):
        eps = ExperimentParameterSet(experiment_id=self.experiment_id, schema=self.schema, pk=parameterset_id)
        eps.delete()

    def form_data(self, parameterset_id):
        data = {}
        params = ExperimentParameter.objects.filter(parameterset=parameterset_id, parameterset__schema=self.schema).values('string_value', 'name__name')
        for param in params:
            data[param['name__name']] = param['string_value']
        return data
        

def _update(parameterset, name, string_value):
    param = _get_or_none(ExperimentParameter.objects.all(), parameterset=parameterset, name=name)
    if string_value:
        if not param:
            param = ExperimentParameter(parameterset=parameterset, name=name)
        param.string_value = string_value
        param.save()
    else:
        if param:
            param.delete()

def _maybe_add(eps, name, value, force=False):
    if value or force:
        ExperimentParameter(parameterset=eps, name=name, string_value=value).save()

def _get_or_none(queryset, **kwargs):
    objs = queryset.filter(**kwargs)
    if len(objs) != 1:
        return None
    else:
        return objs[0]
