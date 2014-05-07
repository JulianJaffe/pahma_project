__author__ = 'Julian Jaffe'

import sys
import json
import pgdb

TIMEOUTCOMMAND = 'set statement_timeout to 500'


class DBConnection:
    def getMatches(self, q, connect_string, srchindex, term, table, expression):
        postgresdb = pgdb.connect(connect_string)
        cursor = postgresdb.cursor()

        if srchindex == 'object':
            TEMPLATE = """SELECT cc.objectnumber
            FROM collectionobjects_common cc
            JOIN collectionobjects_pahma cp ON (cc.id = cp.id)
            JOIN misc ON misc.id = cc.id AND misc.lifecyclestate <> 'deleted'
            WHERE cc.objectnumber like '%s%%'
            ORDER BY cp.sortableobjectnumber LIMIT 30;"""
        else:
            TEMPLATE = TEMPLATE % (term,table,term,expression,term)

        try:
            # double single quotes that appear in the data, to make psql happy
            q = q.replace("'","''")
            query = TEMPLATE % q
            #sys.stderr.write("autosuggest query: %s" % query)
            cursor.execute(query)
            result = []
            for r in cursor.fetchall():
                result.append({'value': r[0]})

            result.append({'s': srchindex})

            #print 'Content-Type: application/json\n\n'
            #prxnt 'debug autosuggest', srchindex,elementID
            return json.dumps(result)    # or "json.dump(result, sys.stdout)"

        except pgdb.DatabaseError, e:
            sys.stderr.write('autosuggest select error: %s' % e)
            return None
        except:
            sys.stderr.write("some other autosuggest database error!")
            return None

    TEMPLATE = """select distinct(%s)
            FROM %s tg
            INNER JOIN hierarchy h_tg ON h_tg.id=tg.id
            INNER JOIN hierarchy h_loc ON h_loc.id=h_tg.parentid
            INNER JOIN misc ON misc.id=h_loc.id AND misc.lifecyclestate <> 'deleted'
            WHERE %s %s ORDER BY %s LIMIT 30;"""