#!/usr/bin/python
 
# doc root /home/users/web/b286/dom.thekrishnans/public_html
# url wluz.com/nytgetcomments.py
import sys, os
from urllib2 import urlopen
import urllib
from json import loads
from json import dumps
import codecs
import time
from datetime import date
import urllib
import cgi
import cgitb; cgitb.enable()  # for troubleshooting via trace backs
#import cgitb; cgitb.enable(display=1, logdir='/home/users/web/b286/dom.thekrishnans/logs',context=5, file=nytgc.txt, format='txt')  # for troubleshooting via trace backs

from nyt1 import ChickenloverDB 

clDB = ChickenloverDB()
nytParams = clDB.getNytUserParams()
url = nytParams['url']
data = nytParams['data']

def call_by_userid(url, data):
    url_values = urllib.urlencode(data)
    full_url = url + "?" + url_values
    response = urlopen(full_url).read()
    return loads(response)
    
print "Content-type: text/html"
print

print """
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> NYT Chickenlover comments load - CGI Script </h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")
#if message == 'chickenlover':
print 'fetching chickenlover comments from NYTimes<br/>'

prev_qtr_begin=time.mktime(date(date.today().year,((date.today().month - 3) % 12),1).timetuple())
print "prev_qtr_begin\t= %s secs  <br/>" % time.asctime(time.localtime(prev_qtr_begin))
comments = call_by_userid(url, data)
total_avail_comments = comments["results"]["totalCommentsFound"]
count_returned_comments = comments["results"]["totalCommentsReturned"]
count_scanned_comments = 0
comment_rec = ""
if count_scanned_comments < total_avail_comments:
    we_have_more_comments=True
    output_file = codecs.open('../../chickenlover/mytest.json','w',encoding='utf-8')
    output_file.write('{"comments": [')
    clDB.cleanup('nyt_comments')
else:
    we_have_more_comments=False

while we_have_more_comments:
    #print count_scanned_comments,'of',total_avail_comments, ' [',count_returned_comments,']<br/>'
    clDB.insertComments(comments["results"]["comments"])
    for c in comments["results"]["comments"]:
        comment_created_on=float(c["createDate"])
        comment_rec += dumps(c)
        output_file.write(comment_rec + "\n")
        comment_rec = ", "
        #print "[%d] [%d] [%s] [%s]<br/>" % (c['commentID'],c['recommendations'],c['asset']['assetTitle'].encode('utf-8'),c['asset']['assetURL'].encode('utf-8'))
        #c['commentBody']

    count_scanned_comments+=count_returned_comments
    #print "last comment_created_on\t= %s <br/>" % time.asctime(time.localtime(comment_created_on))
    if count_scanned_comments < total_avail_comments and comment_created_on > prev_qtr_begin:
       	data['offset'] = count_scanned_comments
        time.sleep(2) # delays for 2 seconds
        comments=call_by_userid(url, data)
        count_returned_comments = comments["results"]["totalCommentsReturned"]
    else:
        comments["results"]["comments"]=[]
        we_have_more_comments=False
        output_file.write(']}')
        output_file.close()

print """

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="nytgetcomments.py">
    <p>message: <input type="text" name="message"/></p>
  </form>
""" % cgi.escape(message)

print """
</body>

</html>
"""