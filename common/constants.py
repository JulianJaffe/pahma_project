# -*- coding: UTF-8 -*-

import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def getProhibitedLocations():
    fileName = 'prohibitedLocations.csv'
    locList = []
    try:
        with open(fileName, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter="\t")
            for row in csvreader:
                locList.append(row[0])
    except:
        print 'FAIL'
        raise

    return locList

def getHandlers():
    handlerslist = [
        ("Lisa Beyer","urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(LisaBeyer1372717980469)'Lisa Beyer'"),
        ("Victoria Bradshaw", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(7267)'Victoria Bradshaw'"),
        ("Zachary Brown","urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(ZacharyBrown1389986714647)'Zachary Brown'"),
        ("Alicja Egbert", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(8683)'Alicja Egbert'"),
        ("Madeleine Fang", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(7248)'Madeleine W. Fang'"),
        ("Leslie Freund", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(7475)'Leslie Freund'"),
        ("Rowan Gard", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(RowanGard1342219780674)'Rowan Gard'"),
        ("Leilani Hunter","urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(LeilaniHunter1389986789001)'Leilani Hunter'"),
        ("Natasha Johnson", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(7652)'Natasha Johnson'"),
        ("Brenna Jordan","urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(BrennaJordan1383946978257)'Brenna Jordan'"),
        ("Corri MacEwen", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(9090)'Corri MacEwen'"),
        ("Karyn Moore","urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(KarynMoore1399567930777)'Karyn Moore'"),
        ("Jon Oligmueller", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(JonOligmueller1372192617217)'Jon Oligmueller'"),
        ("Martina Smith", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(9034)'Martina Smith'"),
        ("Linda Waterfield", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(LindaWaterfield1358535276741)'Linda Waterfield'"),
        ("Jane Williams", "urn:cspace:pahma.cspace.berkeley.edu:personauthorities:name(person):item:name(7420)'Jane L. Williams'")
    ]
    return handlerslist


def getReasons():
    reasonslist = [
        ("(none selected)", "None"),
        ("(not entered)", "(not entered)"),
        ("Inventory", "Inventory"),
        ("General Collections Management", "GeneralCollManagement"),
        ("Research", "Research"),
        ("NAGPRA", "NAGPRA"),
        ("per shelf label", "pershelflabel"),
        ("New Home Location", "NewHomeLocation"),
        ("Loan", "Loan"),
        ("Exhibit", "Exhibit"),
        ("Class Use", "ClassUse"),
        ("Photo Request", "PhotoRequest"),
        ("Tour", "Tour"),
        ("Conservation", "Conservation"),
        ("cultural heritage", "CulturalHeritage"),
        ("2012 HGB surge pre-move inventory", "2012 HGB surge pre-move inventory"),
        ("2014 Marchant inventory and move", "2014 Marchant inventory and move"),
        ("Asian Textile Grant", "AsianTextileGrant"),
        ("Basketry Rehousing Proj", "BasketryRehousingProj"),
        ("BOR Proj", "BORProj"),
        ("Building Maintenance: Seismic", "BuildingMaintenance"),
        ("California Archaeology Proj", "CaliforniaArchaeologyProj"),
        ("Cat. No. Issue Investigation", "CatNumIssueInvestigation"),
        ("Duct Cleaning Proj", "DuctCleaningProj"),
        ("Federal Curation Act", "FederalCurationAct"),
        ("Fire Alarm Proj", "FireAlarmProj"),
        ("First Time Storage", "FirstTimeStorage"),
        ("Found in Collections", "FoundinColl"),
        ("Hearst Gym Basement move to Kroeber 20A", "HearstGymBasementMoveKroeber20"),
        ("HGB Surge", "HGB Surge"),
        ("Kro20Mezz LWeapon Proj 2011", "Kro20MezzLWeaponProj2011"),
        ("Kroeber 20A move to Regatta", "Kroeber20AMoveRegatta"),
        ("Marchant Flood 12/2007", "MarchantFlood2007"),
        ("Native Am Adv Grp Visit", "NAAGVisit"),
        ("NEH Egyptian Collection Grant", "NEHEgyptianCollectionGrant"),
        ("Regatta move-in", "Regattamovein"),
        ("Regatta pre-move inventory", "Regattapremoveinventory"),
        ("Regatta pre-move object prep.", "Regattapremoveobjectprep"),
        ("Regatta pre-move staging", "Regattapremovestaging"),
        ("SAT grant", "SATgrant"),
        ("Temporary Storage", "TemporaryStorage"),
        ("Textile Rehousing Proj", "TextileRehousingProj"),
        ("Yoruba MLN Grant", "YorubaMLNGrant")
    ]

    return reasonslist

def getPrinters():

    printerlist = [
        ("Kroeber Hall", "kroeberBCP"),
        ("Regatta Building", "regattaBCP")
    ]
    return printerlist

def getFieldset():

    fieldlist = [
        ("Key Info", "keyinfo"),
        ("Name & Desc.", "namedesc"),
        ("Registration", "registration"),
        ("HSR Info", "hsrinfo"),
        ("Object Type/CM", "objtypecm"),
        ("Taxonomy", "taxonomy")
    ]
    return fieldlist

def getHierarchies():
    authoritylist = [
        ("Ethnographic Culture", "concept"),
        ("Places", "places"),
        ("Archaeological Culture", "archculture"),
        ("Ethnographic File Codes", "ethusecode"),
        ("Materials", "material_ca"),
        ("Taxonomy", "taxonomy")
    ]
    return authoritylist


def getAltNumTypes():
    altnumtypelist = [
        ("(none selected)", "(none selected)"),
        ("additional number", "additional number"),
        ("attributed pahma number", "attributed PAHMA number"),
        ("burial number", "burial number"),
        ("moac subobjid", "moac subobjid"),
        ("museum number (recataloged to)", "museum number (recataloged to)"),
        ("previous number", "previous number"),
        (u"previous number (albert bender’s number)", "prev. number (Bender)"),
        (u"previous number (bascom’s number)", "prev. number (Bascom)"),
        (u"previous number (collector's original number)", "prev. number (collector)"),
        ("previous number (design dept.)", "prev. number (Design)"),
        ("previous number (mvc number, mossman-vitale collection)", "prev. number (MVC)"),
        ("previous number (ucas: university of california archaeological survey)", "prev. number (UCAS)"),
        ("song number", "song number"),
        ("tag", "tag"),
        ("temporary number", "temporary number"),
        ("associated catalog number", "associated catalog number"),
        ("field number", "field number"),
        ("original number", "original number"),
        ("previous museum number (recataloged from)", "prev. number (recataloged from)"),
        (u"previous number (anson blake’s number)", "prev. number (Blake)"),
        (u"previous number (donor's original number)", "prev. number (donor)"),
        ("previous number (uc paleontology department)", "prev. number (Paleontology)"),
        ("tb (temporary basket) number", "tb (temporary basket) number")

    ]
    return altnumtypelist

def getObjType():
    objtypelist = [
        ("Archaeology", "archaeology"),
        ("Ethnography", "ethnography"),
        ("(not specified)", "(not specified)"),
        ("Documentation", "documentation"),
        ("None (Registration)", "none (Registration)"),
        ("None", "None"),
        ("Sample", "sample"),
        ("Indeterminate", "indeterminate"),
        ("Unknown", "unknown")
    ]
    return objtypelist

def getCollMan():
    collmanlist = [
        ("Natasha Johnson", "Natasha Johnson"),
        ("Leslie Freund", "Leslie Freund"),
        ("Alicja Egbert", "Alicja Egbert"),
        ("Victoria Bradshaw", "Victoria Bradshaw"),
        ("Uncertain", "uncertain"),
        ("None (Registration)", "No collection manager (Registration)")
    ]
    return collmanlist

def getQualifier():
    qualifierlist = [
        ("aff. (genus)", "affg"),
        ("aff. (species)", "aff"),
        ("cf. (genus)", "cfg"),
        ("cf. (species)", "cf"),
        ("indet.", "indet"),
        ("Sp. indet", "spIndet"),
        ("Sp. nov.", "spNov"),
        ("?", "questioned"),
        ("Sensu Latu", "sensuLatu"),
        ("Sensu Stricto", "sensuStricto")
    ]
    return qualifierlist

def getKind():
    kindlist = [
        ("(none selected)", ""),
        ("Original catalog determination", "originalCatalogDetermination"),
        ("Researcher determination", "researcherDetermination"),
        ("Fide", "fide"),
        ("Nomenclatural change", "nomenclaturalChange"),
        ("Taxonomic change", "taxonomicChange")
    ]
    return kindlist

def getAgencies():
    agencylist = [
        ("Bureau of Indian Affairs", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(8452)"),
        ("Bureau of Land Management", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(3784)"),
        ("Bureau of Reclamation", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(6392)"),
        ("California Department of Transportation", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(9068)"),
        ("California State Parks", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(8594)"),
        ("East Bay Municipal Utility District", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(EastBayMunicipalUtilityDistrict1370388801890)"),
        ("National Park Service", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(1533)"),
        ("United States Air Force", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(UnitedStatesAirForce1369177133041)"),
        ("United States Army", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(3021)"),
        ("United States Coast Guard", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(UnitedStatesCoastGuard1342641628699)"),
        ("United States Fish and Wildlife Service", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(UnitedStatesFishandWildlifeService1342132748290)"),
        ("United States Forest Service", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(3120)"),
        ("United States Marine Corps", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(UnitedStatesMarineCorps1365524918536)"),
        ("United States Navy", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(9079)"),
        ("U.S. Army Corps of Engineers", "urn:cspace:pahma.cspace.berkeley.edu:orgauthorities:name(organization):item:name(9133)"),
    ]
    return agencylist