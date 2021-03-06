__author__ = 'jblowe'

import os
import re
import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

from search.utils import doSearch, setConstants, loginfo
from common import cspace # we use the config file reading function
from cspace_django_site import settings
from os import path

config = cspace.getConfig(path.join(settings.BASE_PARENT_DIR, 'config'), 'imaginator')

MAXMARKERS = int(config.get('imaginator', 'MAXMARKERS'))
MAXRESULTS = int(config.get('imaginator', 'MAXRESULTS'))
MAXLONGRESULTS = int(config.get('imaginator', 'MAXLONGRESULTS'))
IMAGESERVER = config.get('imaginator', 'IMAGESERVER')
CSPACESERVER = config.get('imaginator', 'CSPACESERVER')
SOLRSERVER = config.get('imaginator', 'SOLRSERVER')
SOLRCORE = config.get('imaginator', 'SOLRCORE')
TITLE = config.get('imaginator', 'TITLE')
SUGGESTIONS = config.get('imaginator', 'SUGGESTIONS')
LAYOUT = config.get('imaginator', 'LAYOUT')


#@login_required()
def index(request):

    context = setConstants({})

    # http://blog.mobileesp.com/
    # the middleware must be installed for the following to work...
    if request.is_phone:
        context['device'] = 'phone'
    elif request.is_tablet:
        context['device'] = 'tablet'
    else:
        context['device'] = 'other'

    if request.method == 'GET' and request.GET != {}:
        context['searchValues'] = request.GET

        context = setConstants(context)

        if 'text' in request.GET:
            context['text'] = request.GET['text']
        if 'musno' in request.GET:
            context['musno'] = request.GET['musno']
            context['maxresults'] = 1
        if 'submit' in request.GET:
            context['maxresults'] = 20
            if "Metadata" in request.GET['submit']:
                context['resultType'] = 'metadata'
                context['displayType'] = 'full'
            elif "Images" in request.GET['submit']:
                context['resultType'] = 'images'
                context['pixonly'] = 'true'
                context['displayType'] = 'grid'
            elif "Lucky" in request.GET['submit']:
                context['resultType'] = 'metadata'
                context['maxresults'] = 1
        else:
            context['resultType'] = 'metadata'
        context['title'] = TITLE

        # do search
        loginfo('start search', context, request)
        context = doSearch(context)

        return render(request, 'imagineImages.html', context)

    else:
        return render(request, 'imagineImages.html', context)
