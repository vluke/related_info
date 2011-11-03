# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from tardis.tardis_portal.auth import decorators as authz
from tardis.tardis_portal.creativecommonshandler import CreativeCommonsHandler
from tardis.tardis_portal.models import Experiment
from tardis.tardis_portal.shortcuts import render_response_index


from . import forms
from .related_info import RelatedInfoHandler

import logging
logger = logging.getLogger(__name__)


@never_cache
@authz.experiment_access_required
def index(request, experiment_id):
    url = 'related_info/index.html'
    c = Context()
    if request.user.is_authenticated():
        c['has_write_permissions'] = authz.has_write_permissions(request, experiment_id)

    rih = RelatedInfoHandler(experiment_id)
    c['related_uris'] = rih.uris()
    c['related_publications'] = rih.publications()
    c['experiment_id'] = experiment_id

    uris = RelatedInfoHandler(experiment_id)

    return HttpResponse(render_response_index(request, url, c))

@authz.write_permissions_required
def add_uri(request, experiment_id):
    url = 'related_info/add_uri.html'
    c = Context()
    if request.POST:
        pass
    else:
        pass
    return HttpResponse(render_response_index(request, url, c))
    

@authz.write_permissions_required
def add_publication(request, experiment_id):
    url = 'related_info/add_uri.html'
    c = Context()
    if request.POST:
        pass
    else:
        pass
    return HttpResponse(render_response_index(request, url, c))

@authz.write_permissions_required
def edit_uri(request, experiment_id, parameterset_id):
    c = Context()
    pass

@authz.write_permissions_required
def edit_publication(request, experiment_id, parameterset_id):
    c = Context()
    pass

@authz.write_permissions_required
def delete_uri(request, experiment_id, parameterset_id):
    c = Context()
    pass

@authz.write_permissions_required
def delete_publication(request, experiment_id, parameterset_id):
    c = Context()
    pass
