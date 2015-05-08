import urllib2
import time
import sys
import cspace_logging.logging
from common import cspace

try:
    import xml.etree.ElementTree as etree
except ImportError:
    try:
        from lxml import etree
    except ImportError:
        try:
            # normal cElementTree install
            import cElementTree as etree
        except ImportError:
            try:
                # normal ElementTree install
                import elementtree.ElementTree as etree
            except ImportError:
                print("Failed to import ElementTree from any known place")


def updateKeyInfo(fieldset, updateItems, config, user):

    message = ''

    realm = config.get('connect', 'realm')
    hostname = config.get('connect', 'hostname')
    username, password = user.get_username(), user.cspace_password

    uri = 'collectionobjects'
    getItems = updateItems['objectCsid']

    #Fields vary with fieldsets
    if fieldset == 'keyinfo':
        fieldList = ('pahmaFieldCollectionPlace', 'assocPeople', 'objectName', 'pahmaEthnographicFileCode')
    elif fieldset == 'namedesc':
        fieldList = ('briefDescription', 'objectName')
    elif fieldset == 'registration':
        # nb:  'pahmaAltNumType' is handled with  'pahmaAltNum'
        fieldList = ('objectName', 'pahmaAltNum', 'fieldCollector')
    elif fieldset == 'hsrinfo':
        fieldList = ('objectName', 'pahmaFieldCollectionPlace', 'briefDescription')
    elif fieldset == 'objtypecm':
        fieldList = ('objectName', 'collection', 'responsibleDepartment', 'pahmaFieldCollectionPlace')
    elif fieldset == 'taxonomy':
        fieldList = ('objectName', 'taxonomicIdent')#'taxon', 'qualifier', 'identkind', 'identby', 'institution', 'identDate', 'notes')
    else:
        return 'Error! Bad field set'

    # get the XML for this object
    url, content, elapsedtime = getxml(uri, realm, hostname, username, password, getItems)
    root = etree.fromstring(content)
    # add the user's changes to the XML
    for relationType in fieldList:
        # skip if no refName was provided to update
        listSuffix = 'List'
        extra = ''
        if relationType in updateItems and updateItems[relationType] == '':
            continue
        if relationType in ['assocPeople', 'pahmaAltNum', 'taxonomicIdent']:
            extra = 'Group'
        elif relationType in ['briefDescription', 'fieldCollector', 'responsibleDepartment']:
            listSuffix = 's'
        elif relationType in ['collection']:
            listSuffix = ''
        else:
            pass
        metadata = root.findall('.//' + relationType + extra + listSuffix)
        metadata = metadata[0]
        if relationType in ['assocPeople', 'objectName', 'pahmaAltNum', 'taxonomicIdent']:
            if relationType == 'taxonomicIdent':
                print metadata
                new = False
                for element in ['taxon', 'qualifier', 'identKind', 'identBy', 'institution', 'identDate', 'notes']:
                    if not alreadyExists(updateItems[element], metadata.findall('.//' + element)):
                        new = True
                if new:
                    newElement = etree.Element(relationType + 'Group')
                    for element in ['taxon', 'qualifier', 'identKind', 'identBy', 'institution', 'identDate', 'notes']:
                        leafElement = etree.Element(element)
                        leafElement.text = updateItems[element]
                        newElement.append(leafElement)
                    metadata.insert(0, newElement)
            elif not alreadyExists(updateItems[relationType], metadata.findall('.//' + relationType)):
                newElement = etree.Element(relationType + 'Group')
                if relationType == 'taxonomicIdent':
                    for element in ['taxon', 'qualifier', 'identKind', 'identBy', 'institution', 'identDate', 'notes']:
                        leafElement = etree.Element(element)
                        leafElement.text = updateItems[element]
                        newElement.append(leafElement)
                else:
                    leafElement = etree.Element(relationType)
                    leafElement.text = updateItems[relationType]
                    newElement.append(leafElement)
                if relationType in ['assocPeople', 'pahmaAltNum']:
                    apgType = etree.Element(relationType + 'Type')
                    apgType.text = updateItems[relationType + 'Type'].lower() if relationType == 'pahmaAltNum' else 'made by'
                    newElement.append(apgType)
                metadata.insert(0, newElement)
            else:
                # for AltNums, we need to update the AltNumType even if the AltNum hasn't changed
                if relationType == 'pahmaAltNum':
                    apgType = metadata.find('.//' + relationType + 'Type')
                    apgType.text = updateItems[relationType + 'Type']
        elif relationType in ['briefDescription', 'fieldCollector', 'responsibleDepartment']:
            entries = metadata.findall('.//' + relationType)
            if alreadyExists(updateItems[relationType], entries):
                if not IsAlreadyPreferred(updateItems[relationType], entries):
                    message += "%s=%s;" % (relationType,updateItems[relationType])
                continue
            new_element = etree.Element(relationType)
            new_element.text = updateItems[relationType]
            metadata.insert(0,new_element)
            if entries:
                entries.insert(0, new_element)
            else:
                metadata.insert(0, new_element)
        else:
            # check if value is already present. if so, skip
            if alreadyExists(updateItems[relationType], metadata.findall('.//' + relationType)):
                continue
            newElement = etree.Element(relationType)
            newElement.text = updateItems[relationType]
            metadata.insert(0, newElement)
    objectCount = root.find('.//numberOfObjects')
    if 'objectCount' in updateItems:
        if objectCount is None:
            objectCount = etree.Element('numberOfObjects')
            collectionobjects_common = root.find(
                './/{http://collectionspace.org/services/collectionobject}collectionobjects_common')
            collectionobjects_common.insert(0, objectCount)
        objectCount.text = updateItems['objectCount']

    inventoryCount = root.find('.//inventoryCount')
    if 'inventoryCount' in updateItems:
        if inventoryCount is None:
            inventoryCount = etree.Element('inventoryCount')
            collectionobjects_pahma = root.find(
                './/{http://collectionspace.org/services/collectionobject/local/pahma}collectionobjects_pahma')
            collectionobjects_pahma.insert(0, inventoryCount)
        inventoryCount.text = updateItems['inventoryCount']

    collection = root.find('.//collection')
    if 'collection' in updateItems:
        if collection is None:
            collection = etree.Element('collection')
            collectionobjects_common = root.find(
                './/{http://collectionspace.org/services/collectionobject}collectionobjects_common')
            collectionobjects_common.insert(0, collection)
        collection.text = updateItems['collection']

    uri = 'collectionobjects' + '/' + updateItems['objectCsid']
    payload = '<?xml version="1.0" encoding="UTF-8"?>\n' + etree.tostring(root, encoding='utf-8')
    (url, data, csid, elapsedtime) = cspace.postxml(realm, uri, hostname, 'https', '', username, password, payload,
                                                    'PUT', endpoint='services')
    cspace_logging.logging.writeLog(updateItems, uri, 'PUT', username, config)

    return message

def alreadyExists(txt, elements):
    if elements == []: return False
    if type(elements) == type([]):
        for e in elements:
            if txt == str(e.text):
                return True
        return False
    # if we were passed in a single (non-array) Element, just check it..
    if txt == str(elements.text):
        return True
    return False


def IsAlreadyPreferred(txt, elements):
    if elements == []: return False
    if type(elements) == type([]):
        if txt == str(elements[0].text):
            return True
        return False
    # if we were passed in a single (non-array) Element, just check it..
    if txt == str(elements.text):
        return True
    return False


def getxml(uri, realm, hostname, username, password, getItems):
    # port and protocol need to find their ways into the config files...
    port = ''
    protocol = 'https'
    server = protocol + "://" + hostname + port
    passman = urllib2.HTTPPasswordMgr()
    passman.add_password(realm, server, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    if getItems == None:
        url = "%s/cspace-services/%s" % (server, uri)
    else:
        url = "%s/cspace-services/%s/%s" % (server, uri, getItems)
    elapsedtime = 0.0

    try:
        elapsedtime = time.time()
        f = urllib2.urlopen(url)
        data = f.read()
        elapsedtime = time.time() - elapsedtime
    except urllib2.HTTPError, e:
        sys.stderr.write('The server couldn\'t fulfill the request.')
        sys.stderr.write( 'Error code: %s' % e.code)
        raise
    except urllib2.URLError, e:
        sys.stderr.write('We failed to reach a server.')
        sys.stderr.write('Reason: %s' % e.reason)
        raise
    else:
        return (url, data, elapsedtime)


def updateLocations(updateItems, config, realm, hostname, user):
    username, password = user.get_username, user.cspace_password

    uri = 'movements'

    payload = lmiPayload(updateItems)
    (url, data, csid, elapsedtime) = cspace.postxml(realm, uri, hostname, 'https', '', username, password, payload,
                                                    'POST')

    uri = 'relations'

    updateItems['subjectDocumentType'] = 'Movement'
    updateItems['objectDocumentType'] = 'CollectionObject'
    payload = relationsPayload(updateItems)
    (url, data, csid, elapsedtime) = cspace.postxml(realm, uri, hostname, 'https', '', username, password, payload,
                                                    'POST')

    temp = updateItems['objectCsid']
    updateItems['objectCsid'] = updateItems['subjectCsid']
    updateItems['subjectCsid'] = temp
    updateItems['subjectDocumentType'] = 'CollectionObject'
    updateItems['objectDocumentType'] = 'Movement'
    payload = relationsPayload(updateItems)
    (url, data, csid, elapsedtime) = cspace.postxml(realm, uri, hostname, 'https', '', username, password, payload,
                                                    'POST')

    cspace_logging.logging.writeLog(updateItems, uri, 'POST', username, config)


def lmiPayload(f):
    payload = """<?xml version="1.0" encoding="UTF-8"?>
<document name="movements">
<ns2:movements_common xmlns:ns2="http://collectionspace.org/services/movement" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<reasonForMove>%s</reasonForMove>
<currentLocation>%s</currentLocation>
<currentLocationFitness>suitable</currentLocationFitness>
<locationDate>%s</locationDate>
<movementNote>%s</movementNote>
</ns2:movements_common>
<ns2:movements_anthropology xmlns:ns2="http://collectionspace.org/services/movement/domain/anthropology" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<computedSummary>%s</computedSummary>
<crate>%s</crate>
<locationHandlers>
<locationHandler>%s</locationHandler>
</locationHandlers>
</ns2:movements_anthropology>
</document>
"""
    payload = payload % (
        f['reason'], f['locationRefname'], f['locationDate'], f['inventoryNote'], f['computedSummary'], f['crate'],
        f['handlerRefName'])

    return payload


def relationsPayload(f):
    payload = """<?xml version="1.0" encoding="UTF-8"?>
<document name="relations">
  <ns2:relations_common xmlns:ns2="http://collectionspace.org/services/relation" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <relationshipType>affects</relationshipType>
    <objectCsid>%s</objectCsid>
    <objectDocumentType>%s</objectDocumentType>
    <subjectCsid>%s</subjectCsid>
    <subjectDocumentType>%s</subjectDocumentType>
  </ns2:relations_common>
</document>
"""
    payload = payload % (f['objectCsid'], f['objectDocumentType'], f['subjectCsid'], f['subjectDocumentType'])
    return payload