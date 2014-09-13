__author__ = 'jblowe, amywieliczka'

import time, datetime
from os import path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from cspace_django_site.main import cspace_django_site
from utils import writeCsv, doSearch, setupGoogleMap, setupBMapper, setDisplayType, setConstants, loginfo
from appconfig import CSVPREFIX,CSVEXTENSION


# global variables (at least to this module...)

from appconfig import SOLRSERVER, SOLRCORE, PARMS, FIELDS

SEARCHRESULTS = {}


@login_required()
def search(request):
    if request.method == 'GET' and request.GET != {}:
        context = {'searchValues': request.GET}
        context = doSearch(SOLRSERVER, SOLRCORE, context)

        global SEARCHRESULTS
        SEARCHRESULTS = context
    else:
        context = {}

    context = setConstants(context)
    loginfo('start search', context, request)
    return render(request, 'search.html', context)


def retrieveResults(request):
    if request.method == 'POST' and request.POST != {}:
        requestObject = request.POST
        form = forms.Form(requestObject)

        if form.is_valid():
            context = {'searchValues': requestObject}
            context = doSearch(SOLRSERVER, SOLRCORE, context)

            global SEARCHRESULTS
            SEARCHRESULTS = context

            context = setConstants(context)

        loginfo('results.%s' % context['displayType'], context, request)
        return render(request, 'searchResults.html', context)


def bmapper(request):
    if request.method == 'POST' and request.POST != {}:
        requestObject = request.POST
        form = forms.Form(requestObject)

        if form.is_valid():
            context = SEARCHRESULTS
            context = setupBMapper(requestObject, context)

            loginfo('bmapper', context, request)
            return HttpResponse(context['bmapperurl'])


def gmapper(request):
    if request.method == 'POST' and request.POST != {}:
        requestObject = request.POST
        form = forms.Form(requestObject)

        if form.is_valid():
            context = SEARCHRESULTS
            context = setupGoogleMap(requestObject, context)

            loginfo('gmapper', context, request)
            return render(request, 'maps.html', context)


def csv(request):
    if request.method == 'POST' and request.POST != {}:
        requestObject = request.POST
        form = forms.Form(requestObject)

        if form.is_valid():
            # context = {'searchValues': requestObject}
            # context = doSearch(SOLRSERVER, SOLRCORE, context)
            context = SEARCHRESULTS

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s-%s.%s"' % (CSVPREFIX,datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"),CSVEXTENSION)
            #response.write(u'\ufeff'.encode('utf8'))
            writeCsv(response, context['items'], writeheader=True)

            loginfo('csv', context, request)
            return response
