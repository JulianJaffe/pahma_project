#!/usr/bin/env /usr/bin/python

import pgdb
import locale

locale.setlocale(locale.LC_ALL, '')

timeoutcommand = 'set statement_timeout to 300000'

# ############## Overall counts: all Museum number, object and piece counts ######################


def gettotalobjcount(config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    objects = pahmadb.cursor()
    objects.execute(timeoutcommand)

    gettotalobjcount = """
    SELECT * FROM
    (SELECT COUNT(*) AS totalMusNoCount
    FROM collectionobjects_common co
    JOIN collectionobjects_pahma cp ON (co.id=cp.id)
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted' AND cp.iscomponent = 'no') AS totalMusNoCount,
    
    (SELECT COUNT(*) AS totalObjectCount 
    FROM collectionobjects_common co
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted') AS totalObjectCount,

    (SELECT COUNT(objectOverCount.numberofobjects) AS objectOverCount
    FROM (
    SELECT DISTINCT co.objectnumber, co.numberofobjects
    FROM collectionobjects_common co
    JOIN hierarchy h1 ON (co.id = h1.id)
    JOIN relations_common rc ON (h1.name = rc.objectcsid AND rc.subjectdocumenttype='CollectionObject' AND rc.relationshiptype='hasBroader')
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted'
    ) AS objectOverCount) AS objectOverCount,
    
    (SELECT SUM(co.numberofobjects) AS totalPieceCount 
    FROM collectionobjects_common co
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted') AS totalPieceCount,

    (SELECT SUM(pieceOverCount.numberofobjects) AS pieceOverCount
    FROM (
    SELECT DISTINCT co.objectnumber, co.numberofobjects
    FROM collectionobjects_common co
    JOIN hierarchy h1 ON (co.id = h1.id)
    JOIN relations_common rc ON (h1.name = rc.objectcsid AND rc.subjectdocumenttype='CollectionObject' AND rc.relationshiptype='hasBroader')
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted'
    ) AS pieceOverCount) AS pieceOverCount"""
    
    objects.execute(gettotalobjcount)
    return objects.fetchone()

# ############################ Experiment with abstracting the stats querying function ############################


def getgroupedobjcounts(additionaljoin1, additionaljoin2, fieldalias, field, config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    objects = pahmadb.cursor()
    objects.execute(timeoutcommand)

    selectedfield = str(field) + " AS " + str(fieldalias)

    getgroupedobjcounts = """
SELECT %s, MAX(totalMusNoCount) AS totalMusNoCount, MAX(totalObjectCount) AS totalObjectCount, MAX(trueObjectCount) AS trueObjectCount, MAX(totalPieceCount) AS totalPieceCount, MAX(truePieceCount) AS truePieceCount
FROM (
    (SELECT %s, COUNT(*) AS totalMusNoCount, NULL::INTEGER AS totalObjectCount, NULL::INTEGER AS trueObjectCount, NULL::INTEGER AS totalPieceCount, NULL::INTEGER AS truePieceCount
    FROM collectionobjects_common co
    %s
    JOIN collectionobjects_pahma cp ON (co.id=cp.id)
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted' AND cp.iscomponent = 'no'
    GROUP BY %s)
    
    UNION (SELECT %s, NULL::INTEGER AS totalMusNoCount, COUNT(*) AS totalObjectCount, NULL::INTEGER AS trueObjectCount, SUM(co.numberofobjects) AS totalPieceCount, NULL::INTEGER AS truePieceCount
    FROM collectionobjects_common co
    %s
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted'
    GROUP BY %s)
    
    UNION (SELECT %s, NULL::INTEGER AS totalMusNoCount, NULL::INTEGER AS totalObjectCount, COUNT(*) AS trueObjectCount, NULL::INTEGER AS totalPieceCount, SUM(co.numberofobjects) AS truePieceCount
    FROM collectionobjects_common co
    %s
    JOIN misc ON (co.id=misc.id)
    WHERE misc.lifecyclestate <> 'deleted'
    AND co.objectnumber NOT IN
    (   SELECT DISTINCT co.objectnumber
        FROM collectionobjects_common co
        JOIN hierarchy h1 ON (co.id = h1.id)
        JOIN relations_common rc ON (h1.name = rc.objectcsid AND rc.subjectdocumenttype='CollectionObject' AND rc.relationshiptype='hasBroader'))
    GROUP BY %s)
    ) AS collectionCounts
GROUP BY %s
ORDER BY totalMusNoCount DESC""" % (str(fieldalias), str(selectedfield), str(additionaljoin1), str(fieldalias), str(selectedfield), str(additionaljoin2), str(fieldalias), str(selectedfield), str(additionaljoin2), str(fieldalias), str(fieldalias))
    
    objects.execute(getgroupedobjcounts)
    results = objects.fetchall()
    return results

#   ############################ THIS IS AN EXPERIMENT TO GET ONLY LATEST VALUES ##################################
#   ########################## Assumption: only one set of values available per day ###############################


def latestcollectionstats(dbsource, statgroup, config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    objects = pahmadb.cursor()
    objects.execute(timeoutcommand)

    implemented = ['totalCounts', 'objByObjType', 'objByLegCat', 'objByAccStatus', 'objByCollMan', 'objByFileCode', 'objByCntntType', 'objByImgObjType']

    if statgroup not in implemented:
        return "Not Implemented Yet!"

    latestisoruntime = """SELECT MAX(date_trunc('day',isoruntime))
        FROM utils.collectionstats
        WHERE statgroup = '%s'""" % (str(statgroup))

    objects.execute(latestisoruntime)
    latestruntimeresult = objects.fetchone()
    latestruntime = latestruntimeresult[0]
    
    latestcollectionstats = """SELECT label, MAX(musnoval) AS musnoval, MAX(musnopct) AS musnopct, MAX(totobjval) AS totobjval, MAX(totobjpct) AS totobjpct, MAX(truobjval) AS truobjval, MAX(truobjpct) AS truobjpct, MAX(totpcval) AS totpcval, MAX(totpcpct) AS totpcpct, MAX(trupcval) AS trupcval, MAX(trupcpct) AS trupcpct, MAX(isoruntime) AS isoruntime
FROM (
    (SELECT label, statvalue AS "musnoval", statpercent AS "musnopct", NULL::INTEGER AS "totobjval", NULL::INTEGER AS "totobjpct", NULL::INTEGER AS "truobjval", NULL::INTEGER AS "truobjpct", NULL::INTEGER AS "totpcval", NULL::INTEGER AS "totpcpct", NULL::INTEGER AS "trupcval", NULL::INTEGER AS "trupcpct", isoruntime FROM utils.collectionstats
    WHERE dbsource = '%s'
    AND statgroup = '%s'
    AND statmetric = 'totalMusNoCount'
    AND isoruntime >= '%s' 
    ORDER BY label)
    
    UNION (SELECT label, NULL AS "musnoval", NULL AS "musnopct", statvalue AS "totobjval", statpercent AS "totobjpct", NULL AS "truobjval", NULL AS "truobjpct", NULL AS "totpcval", NULL AS "totpcpct", NULL AS "trupcval", NULL AS "trupcpct", isoruntime FROM utils.collectionstats
    WHERE dbsource = '%s'
    AND statgroup = '%s'
    AND statmetric = 'totalObjectCount'
    AND isoruntime >= '%s'
    ORDER BY label)
    
    UNION (SELECT label, NULL AS "musnoval", NULL AS "musnopct", NULL AS "totobjval", NULL AS "totobjpct", statvalue AS "truobjval", statpercent AS "truobjpct", NULL AS "totpcval", NULL AS "totpcpct", NULL AS "trupcval", NULL AS "trupcpct", isoruntime FROM utils.collectionstats
    WHERE dbsource = '%s'
    AND statgroup = '%s'
    AND statmetric = 'trueObjectCount'
    AND isoruntime >= '%s'
    ORDER BY label)
    
    UNION (SELECT label, NULL AS "musnoval", NULL AS "musnopct", NULL AS "totobjval", NULL AS "totobjpct", NULL AS "truobjval", NULL AS "truobjpct", statvalue AS "totpcval", statpercent AS "totpcpct", NULL AS "trupcval", NULL AS "trupcpct", isoruntime FROM utils.collectionstats
    WHERE dbsource = '%s'
    AND statgroup = '%s'
    AND statmetric = 'totalPieceCount'
    AND isoruntime >= '%s'
    ORDER BY label)
    
    UNION (SELECT label, NULL AS "musnoval", NULL AS "musnopct", NULL AS "totobjval", NULL AS "totobjpct", NULL AS "truobjval", NULL AS "truobjpct", NULL AS "totpcval", NULL AS "totpcpct", statvalue AS "trupcval", statpercent AS "trupcpct", isoruntime FROM utils.collectionstats
    WHERE dbsource = '%s'
    AND statgroup = '%s'
    AND statmetric = 'truePieceCount'
    AND isoruntime >= '%s'
    ORDER BY label)
    
) AS latestresults
GROUP BY label
ORDER BY musnoval DESC""" % (str(dbsource), str(statgroup), str(latestruntime), str(dbsource), str(statgroup), str(latestruntime), str(dbsource), str(statgroup), str(latestruntime), str(dbsource), str(statgroup), str(latestruntime), str(dbsource), str(statgroup), str(latestruntime))
    
    objects.execute(latestcollectionstats)
    results = objects.fetchall()
    return results

#   ############################ THIS IS AN EXPERIMENT TO GET ONLY LATEST VALUES FOR ONE TYPE OF COUNT ##################################  I should be able to use latestcollectionstats for this


def lateststatsforstatgroupbycounttype(dbsource, statgroup, statmetric, config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    objects = pahmadb.cursor()
    objects.execute(timeoutcommand)

    latestisoruntime = """SELECT MAX(date_trunc('day',isoruntime))
        FROM utils.collectionstats
        WHERE statgroup = '%s'""" % (str(statgroup))

    objects.execute(latestisoruntime)
    latestruntimeresult = objects.fetchone()
    latestruntime = latestruntimeresult[0]

    latestCounts = """
    SELECT label, statvalue, statpercent, isoruntime, statmetric FROM utils.collectionstats
    WHERE dbsource = '%s'
    AND statgroup = '%s'
    AND statmetric = '%s'
    AND isoruntime >= '%s'
    ORDER BY statvalue DESC""" % (str(dbsource), str(statgroup), str(statmetric), str(latestruntime))
    
    objects.execute(latestCounts)
    count = objects.fetchall()
    return count

#   ######################################################################################################


def dbtransaction(command,config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    cursor = pahmadb.cursor()
    cursor.execute(command)


def getrefname(table,term,config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    objects = pahmadb.cursor()
    objects.execute(timeoutcommand)

    if term == None or term == '':
        return ''

    query = "select refname from %s where refname ILIKE '%%''%s''%%' LIMIT 1" % (table, term)

    try:
        objects.execute(query)
        return objects.fetchone()[0]
    except:
        return ''

#   ######################################################################################################


def getStatSeries(statTarget, category, config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    objects = pahmadb.cursor()
    objects.execute(timeoutcommand)

    statMetric = {'musNumbers': 'totalMusNoCount', 'objects': 'trueObjectCount', 'pieces': 'truePieceCount'}
    try: 
        query = """SELECT isoruntime, statvalue, statmetric, label FROM utils.collectionstats
WHERE statgroup = '%s'
AND stattarget = '%s'
AND statmetric = '%s'
ORDER BY label ASC, isoruntime DESC""" % (category, statTarget, statMetric[statTarget])

        objects.execute(query)
        return objects.fetchall()
    except:
        return 'Query failed (getStatSeries(%s, %s, config)' % (statTarget, category)


def findrefnames(table, termlist, config):

    pahmadb = pgdb.connect(database=config.get('connect', 'connect_string'))
    objects = pahmadb.cursor()
    objects.execute(timeoutcommand)

    result = []
    for t in termlist:
        query = "select refname from %s where refname ILIKE '%%''%s''%%'" % (table, t)

        try:
            objects.execute(query)
            refname = objects.fetchone()
            result.append([t, refname])
        except:
            raise
        return "findrefnames error"

    return result