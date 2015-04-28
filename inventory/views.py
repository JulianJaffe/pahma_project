from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from common.constants import getFieldsets, invHeaders, getAltNumTypes, getCollMan, getObjType, getQualifier, getKind
from connector import db
from common import cspace
from os import path
import time
import inv


@login_required()
def inventory(request):
    context = {'title': 'Inventory'}
    fieldsets = getFieldsets()
    context['fieldsets'] = fieldsets
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    if request.method == 'POST':
        post = request.POST
        if 'fieldset' in post:
            fieldset = post['fieldset']
            context['fieldset'] = fieldset
        else:
            context['error'] = 'Bad Field Set!'
            return render(request, 'inventory.html', context)
        context['searched'] = True
        config_file_name = 'InventoryDev'  # Currently hard-coded Dev
        config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name)
        version = config.get('info', 'version')
        context['version'] = version
        updateType = config.get('info', 'updatetype')
        institution = config.get('info', 'institution')
        protocol = config.get('connect', 'protocol')
        port = config.get('connect', 'port')
        hostname = config.get('connect', 'hostname')
        if fieldset == 'registration':
            context['alt_num_types'] = getAltNumTypes()
        elif fieldset == 'objtypecm':
            context['obj_types'] = getObjType()
            context['coll_mans'] = getCollMan()
        elif fieldset == 'qualifier':
            context['qualifiers'] = getQualifier()
            context['kinds'] = getKind()
        context['headers'] = invHeaders(fieldset)
        inv_parameter = post['by_parameter'] if 'by_parameter' in post else 'by_mus_no'
        context['inv_parameter'] = inv_parameter
        inv_type = post['inventory_type'] if 'inventory_type' in post else 'inv_ind'
        if inv_type not in ['inv_ind', 'inv_bulk']:
            context['error'] = 'Bad Inventory Type!'
            return render(request, 'inventory.html', context)
        context['inv_type'] = inv_type
        if inv_type == 'inv_bulk':
            try:
                start = post['lo.location1']
                end = post['lo.location2'] if 'lo.location2' in post else start
            except KeyError:
                try:
                    start = post['ob.objno1']
                    end = post['ob.objno2'] if 'ob.objno2' in post else start
                except KeyError:
                    start = post['range_start']
                    end = post['range_end'] if 'range_end' in post else start
            context['start'] = start
            context['end'] = end
            return render(request, 'inventory.html', context)
        if inv_parameter == 'by_location':
            #  TODO: Sanitize input to avoid SQLi
            try:
                loc1 = post['lo.location1']
                loc2 = post['lo.location2'] if 'lo.location2' in post else loc1
            except KeyError:
                loc1 = post['range_start']
                loc2 = post['range_end'] if 'range_end' in post else loc1
            context['start'] = loc1
            context['end'] = loc2
            locs = db.getloclist('range', loc1, loc2, 1000, config)
            rowcount = len(locs)
            if rowcount == 0:
                print '<h2>No locations in this range!</h2>'
                return
            totalobjects = 0
            totallocations = 0
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
                        totallocations += 1
                    totalobjects += 1
                    base_link = protocol + '://' + hostname + port + '/collectionspace/ui/' + institution + '/html/%s.html?csid=%s'
                    data = inv.build_data_object(fieldset, r, base_link)
                    locations[l[0]].append(data)
            context['locs'] = sorted(locations.iteritems())
            context['totallocations'] = totallocations
            context['totalobjects'] = totalobjects
        elif inv_parameter == 'by_mus_no':
            #  Todo: Sanitize input to avoid SQLi
            try:
                obj1 = post['ob.objno1']
                obj2 = post['ob.objno2'] if 'ob.objno2' in post else obj1
            except KeyError:
                obj1 = post['range_start']
                obj2 = post['range_end'] if 'range_end' in post else obj1
            context['start'] = obj1
            context['end'] = obj2
            objs = db.getobjlist('range', obj1, obj2, 3000, config)
            context['data'] = []
            totalobjects = 0
            for r in objs:
                totalobjects += 1
                base_link = protocol + '://' + hostname + port + '/collectionspace/ui/' + institution + '/html/%s.html?csid=%s'
                data = inv.build_data_object(fieldset, r, base_link)
                context['data'].append(data)
            context['totalobjects'] = totalobjects
        else:
            context['error'] = 'Bad Parameter!'
            return render(request, 'inventory.html', context)
    return render(request, 'inventory.html', context)


@login_required()
def update(request):
    context = {}
    context['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    if request.method == 'POST':
        post = request.POST
        if 'fieldset' in post:
            fieldset = post['fieldset']
            context['fieldset'] = fieldset
        else:
            context['error'] = 'Bad Field Set!'
            return render(request, 'inventory.html', context)
        config_file_name = 'InventoryDev'  # Currently hard-coded Dev
        config = cspace.getConfig(path.dirname(path.abspath(__file__)), config_file_name)
        version = config.get('info', 'version')
        context['version'] = version
        updateType = config.get('info', 'updatetype')
        institution = config.get('info', 'institution')
        csids = []
        if 'inv_type' in post and post['inv_type'] == 'inv_bulk':
            try:
                if post['inv_parameter'] == 'by_location':
                    locs = db.getloclist('range', post['start'], post['end'], 1000, config)
                    objs = []
                    for l in locs:
                        objs.append(db.getlocations(l[0], '', 1, config, updateType, institution))
                else:
                    objs = db.getobjlist('range', post['start'], post['end'], 3000, config)
            except:
                objs = []

            for row in objs:
                csids.append(row[8])
        else:
            for i in post.keys():
                if 'csid.' in i:
                    csids.append(i[5:])
        context['csids'] = csids
        inv_type = post.get('inv_type', 'inv_ind')
        refnames = inv.getRefNames(post, csids, fieldset, inv_type, config)
        context['refnames'] = refnames
        num_updated, update_items, not_found = inv.do_update(post, fieldset, csids, refnames, inv_type, request.user,
                                                             config)
        messages = {}
        for csid in csids:
            obj_no = db.getCSIDDetail(config, csid, 'objNumber')
            if csid in not_found.keys():
                messages[csid] = "%s Error:" % obj_no
                for key in not_found[csid]:
                    messages[csid] += '<span style="color: red"> %s %s not found, %s not updated!</span>' % \
                                      (inv.TAG_DICT[key], not_found[csid][key], inv.TAG_DICT[key])
            else:
                messages[csid] = "%s updated successfully." % obj_no
        context['messages'] = messages
        context['num_updated'] = num_updated

    return render(request, 'update.html', context)
