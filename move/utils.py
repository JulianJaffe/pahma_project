import re
import datetime
from connector import db, services


def doUpdateLocations(post, request, config):
    notlocated = "urn:cspace:pahma.cspace.berkeley.edu:locationauthorities:name(location):item:name(sl23524)'Not located'"
    updateValues = [post.get(i) for i in post if 'r.' in i]

    # if reason is a refname (e.g. bampfa), extract just the displayname
    reason = post.get('reason')
    reason = re.sub(r"^urn:.*'(.*)'", r'\1', reason)

    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    numUpdated = 0
    res = {'total': 0}
    for row, obj in enumerate(updateValues):

        updateItems = {}
        cells = obj.split('|')
        updateItems['objectStatus'] = cells[0]
        updateItems['objectCsid'] = cells[1]
        updateItems['locationRefname'] = cells[2]
        updateItems['subjectCsid'] = '' # cells[3] is actually the csid of the movement record for the current location; the updated value gets inserted later
        updateItems['objectNumber'] = cells[4]
        updateItems['crate'] = cells[5]
        updateItems['inventoryNote'] = post.get('n.' + cells[4]) if post.get('n.' + cells[4]) else ''
        updateItems['locationDate'] = now
        updateItems['computedSummary'] = updateItems['locationDate'][0:10] + (' (%s)' % reason)

        for i in ('handlerRefName', 'reason'):
            updateItems[i] = post.get(i)

        # ugh...this logic is in fact rather complicated...
        msg = 'location updated.'
        # if we are moving a crate, use the value of the toLocation's refname, which is stored hidden on the post.
        if config.get('info', 'updatetype') == 'movecrate':
            updateItems['locationRefname'] = post.get('toRefname')
            msg = 'crate moved to %s.' % post.get('toLocAndCrate')

        if config.get('info', 'updatetype') in ['moveobject', 'powermove']:
            if updateItems['objectStatus'] == 'do not move':
                msg = "not moved."
            else:
                updateItems['locationRefname'] = post.get('toRefname')
                updateItems['crate'] = post.get('toCrate')
                msg = 'object moved to %s.' % post.get('toLocAndCrate')

        if updateItems['objectStatus'] == 'not found':
            updateItems['locationRefname'] = notlocated
            updateItems['crate'] = ''
            msg = "moved to 'Not Located'."
        try:
            if "not moved" in msg:
                pass
            else:
                realm = config.get('connect', 'realm')
                hostname = config.get('connect', 'hostname')
                services.updateLocations(updateItems, config, realm, hostname, request.user)
                numUpdated += 1
        except:
            msg = '<span style="color:red;">problem updating!</span>'
        res[updateItems['objectNumber']] = [updateItems['objectNumber'], updateItems['objectStatus'],
                                            updateItems['inventoryNote'], msg]
        res['total'] += 1

    res['numUpdated'] = numUpdated
    return res


def build_sys_inv_data_object(obj, base_link):
    """
    :param obj:         The object whose data is being extracted
    :param base_link:   The base Cspace link to be used for creating hyperlinks for museum numbers and accession records
    :return:            A dictionary containing the appropriate values from the OBJ for the the given FIELDSET
    """
    """
[0 Location, 1 Sortable Location, 2 Timestamp, 3 Museum Number, 4 Count, 5 Name, 6 Movement CSID, 7 refname, 8 csid, ...]"""
    link = base_link % ('cataloging', obj[8])
    data = {'csid': obj[8], 'obj_no': obj[3], 'name': obj[5], 'link': link, 'location': obj[0], 'movement_csid': obj[6],
            'refname': obj[7]}
    return data


def build_move_crate_data_object(obj, base_link):
    return {}


def build_move_obj_data_object(obj, base_link):
    return {}


def build_power_move_data_object(obj, base_link):
    return {}


def getLocation(obj):
    return ''


def doCheckMove(post, config, base_link):
    institution = config.get('info', 'institution')

    crate = verifyLocation(post.get("lo.crate"), config)
    fromLocation = verifyLocation(post.get("lo.location1"), config)
    toLocation = verifyLocation(post.get("lo.location2"), config)

    toRefname = db.getrefname('locations_common', toLocation, config)

    # Move validation to views
    if crate == '':
        print '<span style="color:red;">Crate is not valid! Sorry!</span><br/>'
    if fromLocation == '':
        print '<span style="color:red;">From location is not valid! Sorry!</span><br/>'
    if toLocation == '':
        print '<span style="color:red;">To location is not valid! Sorry!</span><br/>'
    if crate == '' or fromLocation == '' or toLocation == '':
        return

    try:
        # NB: the movecrate webapp uses the inventory query...naturally!
        objects = db.getlocations(post.get("lo.location1"), '', 1, config, 'inventory', institution)
    except:
        raise

    locations = {}
    if len(objects) == 0:
        msg = '<span style="color:red;">No objects found at this location! Sorry!</span>'

    totalobjects = 0
    totallocations = 0

    for r in objects:
        if r[15] != crate:  # skip if this is not the crate we want
            continue
        #locationheader = formatRow({'rowtype': 'subheader', 'data': r}, post, config)
        locationheader = getLocation(r)
        if locations.has_key(locationheader):
            pass
        else:
            locations[locationheader] = []
            totallocations += 1

        totalobjects += 1
        #locations[locationheader].append(formatRow({'rowtype': 'inventory', 'data': r}, post, config))
        locations[locationheader].append(build_move_crate_data_object(r, base_link))

    locs = locations.keys()
    locs.sort()

    if len(locs) == 0:
        msg = '<span style="color:red;">Did not find this crate at this location! Sorry!</span>'

    return crate, fromLocation, toLocation, toRefname, locs


def doCheckPowerMove(post, config, base_link):
    institution = config.get('info', 'institution')

    crate1 = verifyLocation(post.get("lo.crate1"), config)
    crate2 = verifyLocation(post.get("lo.crate2"), config)

    fromLocation = verifyLocation(post.get("lo.location1"), config)
    toLocation = verifyLocation(post.get("lo.location2"), config)

    # Move to view
    if crate1 == '':
        print '<span style="color:red;">From Crate is not valid! Sorry!</span><br/>'
    if crate2 == '':
        print '<span style="color:red;">To Crate is not valid! Sorry!</span><br/>'
    if fromLocation == '':
        print '<span style="color:red;">From location is not valid! Sorry!</span><br/>'
    if toLocation == '':
        print '<span style="color:red;">To location is not valid! Sorry!</span><br/>'
    if fromLocation == '' or toLocation == '':
        return

    toLocRefname = db.getrefname('locations_common', toLocation, config)
    toCrateRefname = db.getrefname('locations_common', crate2, config)
    fromRefname = db.getrefname('locations_common', fromLocation, config)

    try:
        # NB: the movecrate webapp uses the inventory query...naturally!
        objects = db.getlocations(post.get("lo.location1"), '', 1, config, 'inventory',institution)
    except:
        raise

    locations = {}
    if len(objects) == 0:
        msg = '<span style="color:red;">No objects found at this location! Sorry!</span>'

    totalobjects = 0
    totallocations = 0

    for r in objects:
        if r[15] != crate1 and crate1 != '': # skip if this is not the crate we want
                continue
        #locationheader = formatRow({'rowtype': 'subheader', 'data': r}, post, config)
        locationheader = getLocation(r)
        if locationheader in locations:
            pass
        else:
            locations[locationheader] = []
            totallocations += 1

        totalobjects += 1
        #locations[locationheader].append(formatRow({'rowtype': 'powermove', 'data': r}, post, config))
        locations[locationheader].append(build_power_move_data_object(r, base_link))

    locs = locations.keys()
    locs.sort()

    if len(locs) == 0:
        msg = '<span style="color:red;">Did not find this crate at this location! Sorry!</span>'

    return crate1, crate2, fromLocation, toLocation, toLocRefname, toCrateRefname, fromRefname, locs


def doObjectSearch(post, config, base_link):
    crate = verifyLocation(post.get("lo.crate"), config)
    toLocation = verifyLocation(post.get("lo.location1"), config)

    # Move error checking to view
    if str(post.get("lo.crate")) != '' and crate == '':
        print '<span style="color:red;">Crate is not valid! Sorry!</span><br/>'
    if toLocation == '':
        print '<span style="color:red;">Destination is not valid! Sorry!</span><br/>'
    if (str(post.get("lo.crate")) != '' and crate == '') or toLocation == '':
        return

    toRefname = db.getrefname('locations_common', toLocation, config)
    toCrate = db.getrefname('locations_common', crate, config)

    try:
        rows = db.getobjlist('range', post.get("ob.objno1"), post.get("ob.objno2"), 500, config)
    except:
        raise

    objs = []

    if len(rows) == 0:
        msg = '<span style="color:red;">No objects in this range! Sorry!</span>'
    else:
        totalobjects = 0
        for r in rows:
            totalobjects += 1
            res = build_move_obj_data_object(r, base_link)
            objs.append(res)

    return crate, toLocation, toRefname, toCrate, objs


def verifyLocation(loc, config):
    location = db.getloclist('exact', loc, '', 1, config)
    if location == []:
        return
    if loc == location[0][0]:
        return loc
    else:
        return ''