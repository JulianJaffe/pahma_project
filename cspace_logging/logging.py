import os
import csv
import datetime
import codecs
import sys


def writeLog(updateItems, uri, httpAction, username, config):
    # Comment out, for now
    '''
    auditFile = config.get('files', 'auditfile')
    updateType = config.get('info', 'updatetype')
    myPid = str(os.getpid())
    # writing of individual log files is now disabled. audit file contains the same data.
    #logFile = config.get('files','logfileprefix') + '.' + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") + myPid + '.csv'

    # yes, it is inefficient open the log to write each row, but in the big picture, it's insignificant
    try:
        #csvlogfh = csv.writer(codecs.open(logFile,'a','utf-8'), delimiter="\t")
        #csvlogfh.writerow([updateItems['locationDate'],updateItems['objectNumber'],updateItems['objectStatus'],updateItems['subjectCsid'],updateItems['objectCsid'],updateItems['handlerRefName']])
        csvlogfh = csv.writer(codecs.open(auditFile, 'a', 'utf-8'), delimiter="\t")
        logrec = [ httpAction, datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), updateType, uri, username ]
        for item in updateItems.keys():
            logrec.append("%s=%s" % (item,updateItems[item]))
        csvlogfh.writerow(logrec)
    except:
        raise
        #print 'writing to log %s failed!' % auditFile
        '''
    pass


def writeInfo2log(request, form, config, elapsedtime):
    # Comment out, for now
    '''
    checkServer = form.get('check')
    location1 = str(form.get("lo.location1"))
    location2 = str(form.get("lo.location2"))
    action = str(form.get("action"))
    serverlabel = config.get('info', 'serverlabel')
    apptitle = config.get('info', 'apptitle')
    updateType = config.get('info', 'updatetype')
    checkServer = form.get('check')
    # override updateType if we are just checking the server
    if checkServer == 'check server':
        updateType = checkServer
    sys.stderr.write('%-13s:: %-18s:: %-6s::%8.2f :: %-15s :: %s :: %s\n' % (updateType, action, request, elapsedtime, serverlabel, location1, location2))
    updateItems = {'app': apptitle, 'server': serverlabel, 'elapsedtime': '%8.2f' % elapsedtime, 'action': action}
    writeLog(updateItems, '', request, '', config)'''