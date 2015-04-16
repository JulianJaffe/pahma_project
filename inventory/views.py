from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from common.constants import getFieldsets, invHeaders, getAltNumTypes, getCollMan, getObjType, getQualifier, getKind
from connector import db, services
from common import cspace
from os import path


# @login_required()
def inventory(request):
    context = {'title': 'Inventory'}
    fieldsets = getFieldsets()
    context['fieldsets'] = fieldsets
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
                    print objects
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
                    data = build_data_object(fieldset, r, base_link)
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
                data = build_data_object(fieldset, r, base_link)
                context['data'].append(data)
            context['totalobjects'] = totalobjects
        else:
            context['error'] = 'Bad Parameter!'
            return render(request, 'inventory.html', context)
    return render(request, 'inventory.html', context)


# @login_required()
def update(request):
    context = {}
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
        csids = []
        refNames2find = {}
        for i in post.keys():
            if 'csid.' in i:
                csids.append(i)

        for row, csid in enumerate(csids):
            index = csid # for now, the index is the csid
            if fieldset == 'namedesc':
                pass
            elif fieldset == 'registration':
                if not refNames2find.has_key(post.get('ant.' + index)):
                    refNames2find[post.get('ant.' + index)] = db.getrefname('pahmaaltnumgroup_type', post.get('ant.' + index), config)
                if not refNames2find.has_key(post.get('collector.' + index)):
                    refNames2find[post.get('collector.' + index)] = db.getrefname('collectionobjects_common_fieldcollectors', post.get('collector.' + index), config)
                if not refNames2find.has_key(post.get('donor.' + index)):
                    refNames2find[post.get('donor.' + index)] = db.getrefname('acquisitions_common_owners', post.get('donor.' + index), config)
            elif fieldset == 'keyinfo':
                if not refNames2find.has_key(post.get('fcp.' + index)):
                    refNames2find[post.get('fcp.' + index)] = db.getrefname('places_common', post.get('fcp.' + index), config)
                if not refNames2find.has_key(post.get('cult.' + index)):
                    refNames2find[post.get('cult.' + index)] = db.getrefname('concepts_common', post.get('cult.' + index), config)
                if not refNames2find.has_key(post.get('efc.' + index)):
                    refNames2find[post.get('efc.' + index)] = db.getrefname('concepts_common', post.get('efc.' + index), config)
            elif fieldset == 'hsrinfo':
                if not refNames2find.has_key(post.get('fcp.' + index)):
                    refNames2find[post.get('fcp.' + index)] = db.getrefname('places_common', post.get('fcp.' + index), config)
            elif fieldset == 'objtypecm':
                if not refNames2find.has_key(post.get('fcp.' + index)):
                    refNames2find[post.get('fcp.' + index)] = db.getrefname('places_common', post.get('fcp.' + index), config)
            elif fieldset == 'taxonomy':
                if not refNames2find.has_key(post.get('taxon.' + index)):
                    refNames2find[post.get('taxon.' + index)] = db.getrefname('taxon_common', post.get('taxon.' + index), config)
                if not refNames2find.has_key(post.get('ident_by.' + index)):
                    refNames2find[post.get('ident_by.' + index)] = db.getrefname('persons_common', post.get('idnet_by.' + index), config)
                if not refNames2find.has_key(post.get('tax_inst.' + index)):
                    refNames2find[post.get('tax_inst.' + index)] = db.getrefname('organizations_common', post.get('tax_inst.' + index), config)
            else:
                pass
                #error! fieldset not set!

            raise Exception(refNames2find)

    return render(request, 'update.html', context)


def build_data_object(fieldset, obj, base_link):
    """
    :param fieldset:    The fieldset to be displayed
    :param obj:         The object whose data is being extracted
    :param base_link:   The base Cspace link to be used for creating hyperlinks for museum numbers and accession records
    :return:            A dictionary containing the appropriate values from the OBJ for the the given FIELDSET
    """
    """
[0 Location, 1 Location Key, 2 Timestamp, 3 Museum Number, 4 Name, 5 Count, 6 Collection Place, 7 Culture, 8 csid,
9 Ethnographic File Code, 10 Place Ref Name, 11 Culture Ref Name, 12 Ethnographic File Code Ref Name, 13 Crate Ref Name,
14 Computed Crate 15 Description, 16 Collector, 17 Donor, 18 Alt Num, 19 Alt Num Type, 20 Collector Ref Name,
21 Accession Number, 22 Donor Ref Name, 23 Acquisition ID, 24 Acquisition CSID, 25 Count Note, 26 Obj Type,
27 Collection Manager, 28 Taxon, 29 Qualifier, 30 Kind, 31 Identified By, 32 Institution, 33 Taxonomic Notes, 34 Date]"""
    link = base_link % ('cataloging', obj[8])
    link2 = base_link % ('acquisition', obj[24])
    data = {'csid': obj[8], 'obj_no': obj[3], 'name': obj[4]}
    if fieldset == 'keyinfo':
        data['count'] = obj[5]
        data['fcp'] = obj[6]
        data['cult'] = obj[7]
        data['efc'] = obj[9]
    elif fieldset == 'namedesc':
        data['desc'] = obj[15]
    elif fieldset == 'registration':
        data['alt_num'] = obj[18]
        data['ant'] = obj[19]
        data['collector'] = obj[16]
        data['donor'] = obj[17]
        data['acc_no'] = obj[21]
        data['link2'] = link2
    elif fieldset == 'hsrinfo':
        data['count'] = obj[5]
        data['count_note'] = obj[25]
        data['fcp'] = obj[6]
        data['desc'] = obj[15]
    elif fieldset == 'objtypecm':
        data['count'] = obj[5]
        data['obj_type'] = obj[26]
        data['coll_man'] = obj[27]
        data['fcp'] = obj[6]
    elif fieldset == 'taxonomy':
        data['taxon'] = obj[28]
        data['qual'] = obj[29]
        data['kind'] = obj[30]
        data['ident_by'] = obj[31]
        data['tax_inst'] = obj[32]
        data['tax_notes'] = obj[33]
        data['date'] = obj[34]
    data['link'] = link
    return data