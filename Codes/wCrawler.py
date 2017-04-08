#coding:utf-8
from bs4 import BeautifulSoup
import urllib2
import urllib
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

number = 0
for number in range(0,2490,30):
	content=urllib2.urlopen("http://www.ipv6forum.com/ipv6_enabled/approval_list.php?start="+str(number)).read()
	soup=BeautifulSoup(content,'html.parser',from_encoding='utf-8')
	websources = soup.findAll('a',attrs={"target":"_blank"})
	for source in websources:
		link = source.get('href')
		print link
