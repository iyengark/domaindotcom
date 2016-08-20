#!/usr/bin/python
 
# doc root /home/users/web/b286/dom.thekrishnans/public_html
# url wluz.com/nyt0.py
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
import cgitb; cgitb.enable(display=1, logdir='/home/users/web/b286/dom.thekrishnans/logs',context=5, file=nyt0.txt, format='txt')  # for troubleshooting via trace backs

from nyt1 import getParams

count = 6
params=getParams()
paramdict = {}
for p2 in params:
     paramdict[p2['name']] = p2['value']

#print "articleUrl\t= %s <br/>" % paramdict['articleUrl']
#print "chickenlover\t= %s <br/>" % paramdict['chickenlover']
#print "newswireApiKey\t= %s <br/>" % paramdict['newswireApiKey']
#print "userApiKey\t= %s <br/>" % paramdict['userApiKey']
#print "userContentUrl\t= %s <br/>" % paramdict['userContentUrl']
url = paramdict['userContentUrl']
data = {}
data['api-key'] = paramdict['userApiKey']
data['userID'] = paramdict['chickenlover']
data['offset'] = 0

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

  <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")
output_file = codecs.open('../../chickenlover/mytest.json','w',encoding='utf-8')
#output_file.write('message: '+message+'\n')
#output_file.write('UNIQUE_ID='+os.environ["UNIQUE_ID"]+'\n')
#output_file.write('DOCUMENT_ROOT='+os.environ["DOCUMENT_ROOT"]+'\n')

prev_qtr_begin=time.mktime(date(date.today().year,((date.today().month - 3) % 12),1).timetuple())
print "prev_qtr_begin\t= %s secs <br/> " % (prev_qtr_begin)
print "asctime(prev_qtr_begin): %s" % time.asctime(prev_qtr_begin)
comments = call_by_userid(url, data)
count = count - 1
total_avail_comments = comments["results"]["totalCommentsFound"]
count_returned_comments = comments["results"]["totalCommentsReturned"]
count_scanned_comments = 0
comment_rec = ""
output_file.write('{"comments": [')
if count_scanned_comments < total_avail_comments:
    we_have_more_comments=True
else:
    we_have_more_comments=False

while we_have_more_comments:
    print count_scanned_comments,'of',total_avail_comments, ' [',count_returned_comments,']'
    for c in comments["results"]["comments"]:
        comment_created_on=float(c["createDate"])
        comment_rec += dumps(c)
        output_file.write(comment_rec + "\n")
        comment_rec = ", "
        time.sleep(5) # delays for 5 seconds

    count_scanned_comments+=count_returned_comments
    print "last comment_created_on\t= %s <br/>" % (comment_created_on)
    if count > 0 and count_scanned_comments < total_avail_comments and comment_created_on > prev_qtr_begin:
        data['offset'] = count_scanned_comments
        comments=call_by_userid(url, data)
        count = count - 1
        count_returned_comments = comments["results"]["totalCommentsReturned"]
    else:
        comments["results"]["comments"]=[]
        we_have_more_comments=False

output_file.write(']}')
output_file.close()

print """

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="nyt0.py">
    <p>message: <input type="text" name="message"/></p>
  </form>
""" % cgi.escape(message)

##for name, value in os.environ.items():
##     print "%s\t= %s <br/>" % (name, value)

print """
</body>

</html>
"""