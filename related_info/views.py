# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from tardis.tardis_portal.auth import decorators as authz
from tardis.tardis_portal.creativecommonshandler import CreativeCommonsHandler
from tardis.tardis_portal.models import Experiment, ExperimentParameter
from tardis.tardis_portal.shortcuts import render_response_index


from . import forms
from .related_info import RelatedInfoHandler

import sys

import logging
logger = logging.getLogger(__name__)

related_info_settings = sys.modules['%s.%s.settings' % (settings.TARDIS_APP_ROOT, 'related_info')]
auxiliary_schema_namespace = related_info_settings.RELATED_OTHER_INFO_SCHEMA_NAMESPACE

def _redirect(experiment_id):
    return redirect(reverse('tardis.tardis_portal.views.view_experiment', args=[experiment_id]))


@never_cache
@authz.experiment_access_required
def index(request, experiment_id):
    template = 'related_info/index.html'
    c = Context()
    if request.user.is_authenticated():
        c['has_write_permissions'] = authz.has_write_permissions(request, experiment_id)

    rih = RelatedInfoHandler(experiment_id)
    c['related_info_list'] = rih.info_list()
    c['experiment_id'] = int(experiment_id)
    c['other_info'] = ExperimentParameter.objects.filter(name__schema__namespace=auxiliary_schema_namespace, parameterset__experiment=experiment_id)

    return HttpResponse(render_response_index(request, template, c))

@authz.write_permissions_required
def add_info(request, experiment_id):
    template = 'related_info/info.html'
    c = Context()
    if request.POST:
        form = forms.RelatedInfoForm(request.POST)
        if form.is_valid():
            RelatedInfoHandler(experiment_id).add_info(form.cleaned_data)
            return _redirect(experiment_id)
    else:
        form = forms.RelatedInfoForm()
    c['url'] = reverse('tardis.apps.related_info.views.add_info', args=[experiment_id])
    c['form'] = form
    return HttpResponse(render_response_index(request, template, c))

@authz.write_permissions_required
def edit_info(request, experiment_id, parameterset_id):
    template = 'related_info/info.html'
    c = Context()
    rih = RelatedInfoHandler(experiment_id)
    if request.POST:
        form = forms.RelatedInfoForm(request.POST)
        if form.is_valid():
            rih.edit_info(form.cleaned_data, parameterset_id)
            return _redirect(experiment_id)
    else:
        form = forms.RelatedInfoForm(initial=rih.form_data(parameterset_id))
    c['form'] = form
    c['url'] = reverse('tardis.apps.related_info.views.edit_info', args=[experiment_id, parameterset_id])
    return HttpResponse(render_response_index(request, template, c))

@require_POST
@authz.write_permissions_required
def delete_info(request, experiment_id, parameterset_id):
    rih = RelatedInfoHandler(experiment_id)
    rih.delete_info(parameterset_id)
    return HttpResponse('{"success": true}', mimetype='application/json');
