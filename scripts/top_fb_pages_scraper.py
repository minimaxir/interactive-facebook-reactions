import requests
import json
import csv
import time
import re
import os
from bs4 import BeautifulSoup, Comment

def request_until_succeed(url, if_404_exit = False, seconds_sleep_after_request = 0):
	
	success = False
	while success is False:
		try: 	
			req = requests.get(url)
			time.sleep(seconds_sleep_after_request)
			if req.status_code == 200:
				success = True
		except Exception, e:
			print e
			time.sleep(1)
			
			print "Error for URL %s: %s" % (url, datetime.datetime.now())
			
			is_404 = '404' in str(e)
			if if_404_exit & is_404:
				return '';
			
	return req.text
	
def unicode_normalize(text):
	return text.translate(dict.fromkeys([0x201c, 0x201d, 0x2011, 0x2013, 0x2014, 0x2018, 0x2019, 0x2026, 0x2032])).encode('utf-8')
	
num_pages=8
	


with open('top_fb_pages.txt', 'wb') as file:

	for pagenum in xrange(num_pages):
		url = "http://fanpagelist.com/category/top_users/view/list/sort/talking_about/page%s" % (pagenum+1)
	
		if url is not None:
			soup = BeautifulSoup(request_until_succeed(url), "lxml")
			if soup is None:
				continue;
			
			fb_pages = soup.findAll('li', {'class' : 'ranking_results'})
						
			for fb_page in fb_pages:
				href = fb_page.findAll('a')[1]['href']
				file.write(href.split('/')[2] + "\n")
			