from connector import db, services


TAG_DICT = {'cult': 'Associated Culture', 'count': 'Count', 'fcp': 'Field Collection Place',
            'efc': 'Ethnographic Field Code', 'collector': 'Collector', 'taxon': 'Taxon', 'identBy': 'Identifier',
            'institution': 'Institution'}


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


def getRefNames(post, csids, fieldset, inv_type, config):
    refNames2find = {}

    for csid in csids:
        if inv_type == 'inv_bulk':
            index = 'user'
        else:
            index = csid

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
                refNames2find[post.get('ident_by.' + index)] = db.getrefname('persons_common', post.get('ident_by.' + index), config)
            if not refNames2find.has_key(post.get('tax_inst.' + index)):
                refNames2find[post.get('tax_inst.' + index)] = db.getrefname('organizations_common', post.get('tax_inst.' + index), config)
        else:
            pass
            #error! fieldset not set!

    return refNames2find


def do_update(post, fieldset, csids, refNames2find, inv_type, user, config):
    numUpdated = 0
    temp_update = {}
    temp_nf = {}
    for row, csid in enumerate(csids):

        if inv_type == 'inv_bulk':
            index = 'user'
        else:
            index = csid
        updateItems = {}
        updateItems['objectCsid'] = csid
        updateItems['objectName'] = post.get('name.' + index)
        if fieldset == 'namedesc':
            updateItems['briefDescription'] = post.get('desc.' + index)
        elif fieldset == 'registration':
            updateItems['pahmaAltNum'] = post.get('alt_num.' + index)
            updateItems['pahmaAltNumType'] = post.get('ant.' + index)
            updateItems['fieldCollector'] = refNames2find[post.get('collector.' + index)]
        elif fieldset == 'keyinfo':
            if post.get('count.' + index) != '':
                updateItems['objectCount'] = post.get('count.' + index)
            updateItems['pahmaFieldCollectionPlace'] = refNames2find[post.get('fcp.' + index)]
            updateItems['assocPeople'] = refNames2find[post.get('cult.' + index)]
            updateItems['pahmaEthnographicFileCode'] = refNames2find[post.get('efc.' + index)]
        elif fieldset == 'hsrinfo':
            if post.get('count.' + index) != '':
                updateItems['objectCount'] = post.get('count.' + index)
            updateItems['inventoryCount'] = post.get('count_note.' + index)
            updateItems['pahmaFieldCollectionPlace'] = refNames2find[post.get('fcp.' + index)]
            updateItems['briefDescription'] = post.get('desc.' + index)
        elif fieldset == 'objtypecm':
            updateItems['collection'] = post.get('obj_type.' + index)
            updateItems['responsibleDepartment'] = post.get('coll_man.' + index)
            updateItems['pahmaFieldCollectionPlace'] = refNames2find[post.get('fcp.' + index)]
        elif fieldset == 'taxonomy':
            updateItems['taxon'] = post.get('taxon.' + index)
            updateItems['qualifier'] = post.get('qual.' + index)
            updateItems['identKind'] = post.get('kind.' + index)
            updateItems['identBy'] = post.get('ident_by.' + index)
            updateItems['institution'] = post.get('tax_inst.' + index)
            updateItems['identDate'] = post.get('date.' + index)
            updateItems['notes'] = post.get('tax_notes.' + index)
        else:
            pass
            #error!

        for i in ('handlerRefName',):
            updateItems[i] = post.get(i)

        not_found = {}
        if fieldset == 'keyinfo':
            if updateItems['pahmaFieldCollectionPlace'] == '' and post.get('fcp.' + index):
                if post.get('fcp.' + index) == db.getCSIDDetail(config, index, 'fieldcollectionplace'):
                    pass
                else:
                    not_found['fcp'] = post.get('fcp.' + index)
            if updateItems['assocPeople'] == '' and post.get('cult.' + index):
                if post.get('cult.' + index) == db.getCSIDDetail(config, index, 'assocpeoplegroup'):
                    pass
                else:
                    not_found['cult'] = post.get('cult.' + index)
            if updateItems['pahmaEthnographicFileCode'] == '' and post.get('efc.' + index):
                not_found['efc'] = post.get('efc.' + index)
            if 'objectCount' in updateItems:
                try:
                    int(updateItems['objectCount'])
                    int(updateItems['objectCount'][0])
                except ValueError:
                    not_found['count'] = post.get('count.' + index)
                    del updateItems['objectCount']
        elif fieldset == 'registration':
            if updateItems['fieldCollector'] == '' and post.get('collector.' + index):
                not_found['collector'] = post.get('collector.' + index)
        elif fieldset == 'hsrinfo':
            if updateItems['pahmaFieldCollectionPlace'] == '' and post.get('fcp.' + index):
                if post.get('fcp.' + index) == db.getCSIDDetail(config, index, 'fieldcollectionplace'):
                    pass
                else:
                    not_found['fcp'] = post.get('fcp.' + index)
            if 'objectCount' in updateItems:
                try:
                    int(updateItems['objectCount'])
                    int(updateItems['objectCount'][0])
                except ValueError:
                    not_found['count'] = post.get('count.' + index)
                    del updateItems['objectCount']
        elif fieldset == 'objtypecm':
            if updateItems['pahmaFieldCollectionPlace'] == '' and post.get('fcp.' + index):
                if post.get('fcp.' + index) == db.getCSIDDetail(config, index, 'fieldcollectionplace'):
                    pass
                else:
                    not_found['fcp'] = post.get('fcp.' + index)
            if 'objectCount' in updateItems:
                try:
                    int(updateItems['objectCount'])
                    int(updateItems['objectCount'][0])
                except ValueError:
                    not_found['count'] = post.get('count.' + index)
                    del updateItems['objectCount']
            elif fieldset == 'taxonomy':
                if updateItems['taxon'] == '' and post.get('taxon.' + index):
                    if post.get('taxon.' + index) == db.getCSIDDetail(config, index, 'taxon'):
                        pass
                    else:
                        not_found['taxon'] = post.get('taxon.' + index)
                if updateItems['identBy'] == '' and post.get('ident_by.' + index):
                    if post.get('ident_by.' + index) == db.getCSIDDetail(config, index, 'person'):
                        pass
                    else:
                        not_found['ident_by'] = post.get('ident_by.' + index)
                if updateItems['institution'] == '' and post.get('tax_inst.' + index):
                    if post.get('organization.' + index) == db.getCSIDDetail(config, index, 'organization'):
                        pass
                    else:
                        not_found['institution'] = post.get('organization.' + index)
                if 'objectCount' in updateItems:
                    try:
                        int(updateItems['objectCount'])
                        int(updateItems['objectCount'][0])
                    except ValueError:
                        not_found['count'] = post.get('count.' + index)
                        del updateItems['objectCount']
        try:
            #payload = services.updateKeyInfo(fieldset, updateItems, config, user)
            updateMsg = services.updateKeyInfo(fieldset, updateItems, config, user)
            if updateMsg:
                not_found['update'] = updateMsg
            numUpdated += 1
            temp_update[index] = updateItems
            if not_found:
                temp_nf[index] = not_found
        except:
            raise
    return numUpdated, temp_update, temp_nf
