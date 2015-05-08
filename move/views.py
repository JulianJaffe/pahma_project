from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from common.constants import getHandlers, getReasons
from connector import db
from common import cspace
from os import path
import time
from move import utils


@login_required()
def move_list(request):
    context = {'title': 'Move Webapps',
               'webapps': [['Move', 'move'], ['Power Move', 'power_move'], ['Systematic Inventory', 'sys_inv']],
               'timestamp': time.strftime("%b %d %Y %H:%M:%S", time.localtime()), 'server': 'Dev'}
    return render(request, 'move_list.html', context)


@login_required()
def move(request):
    context = {'title': 'Move'}
    reasons = getReasons()
    handlers = getHandlers()
    context['reasons'] = reasons
    context['handlers'] = handlers
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    server = 'Dev'  # Currently hard-coded
    context['server'] = server
    config_file_name = 'Move'
    config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name + server)
    version = config.get('info', 'version')
    context['version'] = version
    return render(request, 'move.html', context)


@login_required()
def power_move(request):
    pass


@login_required()
def sys_inv(request):
    context = {'title': 'Systematic Inventory'}
    reasons = getReasons()
    handlers = getHandlers()
    context['reasons'] = reasons
    context['handlers'] = handlers
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    server = 'Dev'  # Currently hard-coded
    context['server'] = server
    config_file_name = 'SysInv'
    config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name + server)
    version = config.get('info', 'version')
    context['version'] = version
    if request.method == 'POST':
        post = request.POST
        if 'reason' in post:
            if post['reason'] == 'None':
                context['error'] = 'Please enter a valid reason!'
            reason = post['reason']
            context['reason'] = reason
        else:
            context['error'] = 'Bad Reason!'
        if 'handler' in post:
            if post['handler'] == 'None':
                context['error'] = 'Please select a handler!'
            handler = post['handler']
            context['handler'] = handler
        else:
            context['error'] = 'Bad Handler!'
        if 'error' in context:
            return render(request, 'sys_inv.html', context)
        context['searched'] = False if ('searched' in post and post['searched'] == 'False') else True
        updateType = config.get('info', 'updatetype')
        institution = config.get('info', 'institution')
        protocol = config.get('connect', 'protocol')
        port = config.get('connect', 'port')
        hostname = config.get('connect', 'hostname')
        try:
            loc1 = post['lo.location1']
            loc2 = post['lo.location2'] if ('lo.location2' in post and post['lo.location2']) else loc1
        except KeyError:
            context['error'] = 'Bad Location(s)!'
            return render(request, 'sys_inv.html', context)
        context['start'] = loc1
        context['end'] = loc2
        locs = db.getloclist('range', loc1, loc2, 1000, config)
        rowcount = len(locs)
        if rowcount == 0:
            context['error'] = 'No locations in this range!'
        locations = {}
        for l in locs:
            try:
                objects = db.getlocations(l[0], '', 1, config, updateType, institution)
            except:
                raise
            rowcount = len(objects)
            if rowcount == 0:
                locations[l[0]] = []
            for r in objects:
                if l[0] in locations:
                    pass
                else:
                    locations[l[0]] = []
                base_link = protocol + '://' + hostname + port + '/collectionspace/ui/' + institution + '/html/%s.html?csid=%s'
                data = utils.build_sys_inv_data_object(r, base_link)
                locations[l[0]].append(data)
        context['locs'] = sorted(locations.iteritems())
    return render(request, 'sys_inv.html', context)


@login_required()
def sys_inv_update(request):
    context = {'title': 'Systematic Inventory', 'timestamp': time.strftime("%b %d %Y %H:%M:%S", time.localtime())}
    server = 'Dev'  # Currently hard-coded
    context['server'] = server
    config_file_name = 'SysInv'
    config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name + server)
    version = config.get('info', 'version')
    context['version'] = version
    if request.method == 'POST':
        post = request.POST
        context['post'] = post
        if 'reason' in post:
            if post['reason'] == 'None':
                context['error'] = 'Please enter a valid reason!'
            reason = post['reason']
            context['reason'] = reason
        else:
            context['error'] = 'Bad Reason!'
        if 'handler' in post:
            if post['handler'] == 'None':
                context['error'] = 'Please select a handler!'
            handler = post['handler']
            context['handler'] = handler
        else:
            context['error'] = 'Bad Handler!'
        if 'error' in context:
            return render(request, 'sys_inv_update.html', context)
        try:
            loc1 = post['lo.location1']
            loc2 = post['lo.location2'] if ('lo.location2' in post and post['lo.location2']) else loc1
        except KeyError:
            context['error'] = 'Bad Location(s)!'
            return render(request, 'sys_inv_update.html', context)
        context['start'] = loc1
        context['end'] = loc2
        res = utils.doUpdateLocations(post, request, config)
        context['res'] = res
    return render(request, 'sys_inv_update.html', context)
