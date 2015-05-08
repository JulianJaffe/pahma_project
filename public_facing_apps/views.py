import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from common import cspace
from os import path
import collection_stats as collstats
import time


# @login_required()
def list_apps(request):
    # Build list
    context = {'title': 'Public Facing Apps', 'webapps': [['Collection Stats', 'collection_stats']]}
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    context['server'] = 'Dev'
    return render(request, 'pfa_list.html', context)


# @login_required()
def collection_stats(request):
    context = {}
    codes = [{'code': 'total', 'long': 'Total Counts'},{'code': 'cont', 'long': 'Continent'},
             {'code': 'obj', 'long': 'Object Type'}, {'code': 'cat', 'long': 'Catalog'},
             {'code': 'acc', 'long': 'Accession Status'}, {'code': 'efc', 'long': 'Ethnographic Use Code'},
             {'code': 'coll', 'long': 'Collection Manager'}, {'code': 'iot', 'long': 'Objects Photographed'}]
    server = 'Prod'
    config_file_name = 'CollectionStats'
    config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name + server)
    dbsource = 'pahma.cspace.berkeley.edu'
    total = collstats.getTopStats(dbsource, config)
    context['title'] = 'Collection Stats'
    context['total'] = total
    logo = config.get('info', 'logo')
    context['logo'] = logo
    schemacolor1 = config.get('info', 'schemacolor1')
    context['schemacolor1'] = schemacolor1
    serverlabel = config.get('info', 'serverlabel')
    context['serverlabel'] = serverlabel
    serverlabelcolor = config.get('info', 'serverlabelcolor')
    context['serverlabelcolor'] = serverlabelcolor
    divsize = '''<div id="sidiv" style="position:relative; width:1300px; height:750px; color:black; ">'''
    context['divsize'] = divsize
    for code in codes:
        if code in ['cont', 'obj', 'cult', 'don','acc', 'coll', 'iot']:  # Pie Charts
            code['chartsrc'] = 'piechart.png'
            code['chart_alt'] = 'View Pie Chart'
        elif code == 'total':  # Intoductory Text
            code['chartsrc'] = 'introduction.png'
            code['chart_alt'] = 'Introduction to the Collection'
        elif code in ['cat', 'efc']:  # Bar Charts
            code['chartsrc'] = 'barchart.png'
            code['chart_alt'] = 'View Bar Chart'
        else:
            code['chartsrc'] = 'piechart.png'
            code['chart_alt'] = 'Not Implemented Yet!'
        if code in ['total', 'cont', 'obj', 'cult', 'cat', 'don','acc', 'efc', 'coll', 'iot']:  # Everything, for now
            code['timesrc'] = 'timeseries.png'
            code['time_alt'] = 'View Time Series'
        else:
            code['timesrc'] = 'timeseries.png'
            code['time_alt'] = 'Not Implemented Yet!'
        if code in ['cont', 'obj', 'cult', 'cat', 'don','acc', 'efc', 'coll', 'iot']:
            code['tablesrc'] = 'table.png'
            code['table_alt'] = 'View Table'
        elif code == 'total':
            code['tablesrc'] = 'howtouse.png'
            code['table_alt'] = 'How To Use'
        else:
            code['tablesrc'] = 'table.png'
            code['table_alt'] = 'Not Implemented Yet!'

        code['chart'] = collstats.makeChart(code['code'], dbsource, config)
        code['table'] = collstats.makeTable(code['code'], code['long'], dbsource, config)
        code['time'] = collstats.makeTime(code['code'], config)
    context['codes'] = codes
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    return render(request, 'collection_stats.html', context)