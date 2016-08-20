#!/usr/bin/python
 
# doc root /home/users/web/b286/dom.thekrishnans/public_html
# url wluz.com/cgi-bin/nyt1.py
import sys, os
import time
from datetime import date
import cgi
import cgitb; cgitb.enable()  # for troubleshooting via trace backs
import MySQLdb

class ChickenloverDB:

 def __init__(self):
    try:
      self.conn = MySQLdb.connect (
      host = "t*k*s.domaincommysql.com",
      user = "wluz******",
      passwd = "******",
      db = "params")
      self.cursor = self.conn.cursor()

    except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

 def __del__(self):
        self.conn.close()

 #CleanUp Operation
 def cleanup(self, table):
    print "Deleting table %s <br/>" % (table)
    query = "DELETE FROM " + table
    try:
            self.cursor.execute(query)
            self.conn.commit()
    except MySQLdb.Error, e:
            #print "Error: unable to delete table"
            print "Error %d: %s <br/>" % (e.args[0], e.args[1])
            #print "<br/>query = [%s]<br/>" % query
            self.conn.rollback()

 def insert(self, query, data):
        try:
            self.cursor.execute(query, data)
            #print "%d rows were inserted<br/>" % self.cursor.rowcount
            self.conn.commit()
        except MySQLdb.Error, e:
            #print "Error: unable to insert data"
            print "<br/>Error %d: %s <br/>" % (e.args[0], e.args[1])
            print "<br/>query = [%s]<br/>" % query
            self.conn.rollback()

 def query(self, query):
        cursor = self.conn.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(query)
        return cursor.fetchall()

 def getParams(self):
    #try:
      #conn = MySQLdb.connect (
      #host = "thekrishnans.domaincommysql.com",
      #user = "wluzdotcom",
      #passwd = "netcom",
      #db = "params")

    #except MySQLdb.Error, e:
     #print "Error %d: %s" % (e.args[0], e.args[1])
     #sys.exit (1)

    # prepare a cursor object using cursor() method
    #access data using column index
    #cursor = conn.cursor()
    #access data using column name
    #cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
    # Prepare SQL query to READ a record from params database.
    sql = "SELECT * FROM nyt_params"
    #sql = "SELECT * FROM nyt_params \
    #       WHERE name = '%s'" % ("chickenlover")

    #try:
       # Execute the SQL command
       #cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       #params = cursor.fetchall()
       #for param in params:
          #name = param[0]
          #value = param[1]
          # Now print fetched result
          #print "%s\t= %s <br/>" % \
          #       (name, value)
    #except:
       #print "Error: unable to fetch params data"

    # disconnect from DB server
    #self.conn.close()
    #return params
    return self.query(sql)
 
 def getNytUserParams(self):
    paramdict = {}
    params = self.getParams()
    for p2 in params:
         paramdict[p2['name']] = p2['value']

    data = {}
    data['api-key'] = paramdict['userApiKey']
    data['userID'] = paramdict['chickenlover']
    data['offset'] = 0
    nytParams = {}
    nytParams['url'] = paramdict['userContentUrl']
    nytParams['data'] = data
    return nytParams

 def insertComments(self, comments):
    # Data Insert into the table
    for c in comments:
        #print "[%d] [%d] [%s] [%s]<br/>" % (c['commentID'],c['recommendations'],c['asset']['assetTitle'].encode('utf-8'),c['asset']['assetURL'].encode('utf-8'))
        #c['commentBody']
        query = "INSERT INTO nyt_comments VALUES(%s,%s,\"%s\",\"%s\",\"%s\")" 
        self.insert(query, ( c['commentID'],c['recommendations'],c['asset']['assetTitle'].encode('utf-8'),c['asset']['assetURL'].encode('utf-8'),c['commentBody'].encode('utf-8') ))
