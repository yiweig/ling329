import urllib2
import re

term = 2015
url = 'http://www.mathcs.emory.edu/classes-semester.php?subject=CS&year=2015&term=2&graduate=0'

request = urllib2.Request(url)
response = urllib2.urlopen(request)
page = response.read()
kb = dict()