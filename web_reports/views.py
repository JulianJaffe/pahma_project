import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from common.constants import getAgencies, getHierarchies
from connector import db
from common import cspace
from os import path
from cspace_django_site import settings
import concept_dict_builder as concept
import re
import time


# @login_required()
def list_apps(request):
    # Build list
    context = {'title': 'Web Reports', 'reports': [['Government Holdings', 'government_holdings'],
                                                   ['Hierarchy Viewer', 'hierarchy_viewer'],
                                                   ['Packing List', 'packing_list']]}
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    context['server'] = 'Dev'
    return render(request, 'list.html', context)


# @login_required()
def hierarchy_viewer(request):
    context = {'title': 'Hierarchy Viewer'}
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    hierarchies = getHierarchies()
    context['hierarchies'] = hierarchies
    server = 'Prod'
    context['server'] = server
    if "hierarchy" in request.GET:
        hierarchy = request.GET["hierarchy"]
        if hierarchy not in [h[1] for h in hierarchies]:
            return render(request, 'hierarchy_viewer.html', context)
        context['selected_hierarchy'] = hierarchy
        config_file_name = 'HierarchyViewer'
        config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name + server)
        version = config.get('info', 'version')
        context['version'] = version
        res = db.gethierarchy(hierarchy, config)
        lookup = {concept.PARENT: concept.PARENT}
        hostname = config.get('connect', 'hostname')
        institution = config.get('info', 'institution')
        port = config.get('connect', 'port')
        protocol = config.get('connect', 'protocol')
        link = protocol + '://' + hostname + port + '/collectionspace/ui/' + institution
        if hierarchy == 'taxonomy':
            link += '/html/taxon.html?csid=%s'
        elif hierarchy == 'places':
            link += '/html/place.html?csid=%s'
        else:
            link += '/html/concept.html?csid=%s&vocab=' + hierarchy
        for row in res:
            pretty_name = row[0].replace('"', "'")
            if len(pretty_name) > 0 and pretty_name[0] == '@':
                pretty_name = '<' + pretty_name[1:] + '> '
            pretty_name = pretty_name + '", url: "' + link % (row[2])
            lookup[row[2]] = pretty_name
        res = concept.buildJSON(concept.buildConceptDict(res), 0, lookup)
        data = re.sub(r'\n { label: "(.*?)"},', r'''\n { label: "no parent >> \1"},''', res)
        context['data'] = data
    return render(request, 'hierarchy_viewer.html', context)


# @login_required()
def government_holdings(request):
    context = {'title': 'Government Holdings'}
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    agencies = getAgencies()
    short_agencies = [agency[0] for agency in agencies]
    opt_agencies = [ag.replace(" ", "") for ag in short_agencies]
    context['agencies'] = zip(short_agencies, opt_agencies)
    server = 'Dev'  # Currently hard-coded
    context['server'] = server
    if "agency" in request.GET:
        agency = request.GET["agency"]
        if agency not in opt_agencies:
            return render(request, 'government_holdings.html', context)
        config_file_name = 'GovernmentHoldings'
        config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name + server)
        version = config.get('info', 'version')
        context['version'] = version
        context['selected_agency'] = agency
        pretty_agency = [ag[1] for ag in zip(opt_agencies, short_agencies) if ag[0] == agency][0]
        refname = [ag[1] for ag in agencies if ag[0] == pretty_agency][0]
        context['refname'] = refname
        display_name = db.getDisplayName(config, refname)[0]
        context['display_name'] = display_name
        hostname = config.get('connect', 'hostname')
        institution = config.get('info', 'institution')
        protocol = config.get('connect', 'protocol')
        port = config.get('connect', 'port')
        link = protocol + '://' + hostname + port + '/collectionspace/ui/'+institution+'/html/place.html?csid='
        sites = db.getSitesByOwner(config, refname)
        link_sites = []
        for site in sites:
            site_link = link + str(db.getCSID('placeName', site[0], config)[0]) + '&vocab=place'
            s = site + [site_link]
            link_sites.append(s)
        context['sites'] = link_sites
    return render(request, 'government_holdings.html', context)


# @login_required()
def packing_list(request):
    context = {}
    return render(request, 'packing_list.html', context)


def csv(request):
    """if request.method == 'POST' and request.POST != {}:
        requestObject = dict(request.POST.iteritems())
        form = forms.Form(requestObject)

        if form.is_valid():
            context = {'searchValues': requestObject}
            csvitems = setupCSV(requestObject, context)

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s-%s.%s"' % (CSVPREFIX, datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"), CSVEXTENSION)
            #response.write(u'\ufeff'.encode('utf8'))
            writeCsv(response, csvitems, writeheader=True)
            loginfo('csv', context, request)
            return response"""
    pass
