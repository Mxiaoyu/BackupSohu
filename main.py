#!/usr/bin/python
# -*- coding: utf-8 -*-

# author: majianwei
# date: 2016-03-16

'''back up http://m.sohu.com once 60 seconds.
'''

import os
import sys
import time
import datetime
import urllib
import urllib2
from bs4 import BeautifulSoup


class Backup(object):
	'''deal with the download of page, css, js, image
	'''
	def __init__(self, t, url, path):
		'''initiation
		t: frequency
		url: the url to save
		path: the path to back up to
		'''
		self.t = t
		self.url = url
		self.path = path
		self.now_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
		self.index = self.path + '/' + self.now_time
		self.img = self.path+'/'+self.now_time+'/img'
		self.js = self.path+'/'+self.now_time+'/js'
		self.css = self.path+'/'+self.now_time+'/css'
		# create dir
		if not os.path.exists(self.index):
			os.makedirs(self.index)
		if not os.path.exists(self.img):
			os.makedirs(self.img)
		if not os.path.exists(self.js):
			os.makedirs(self.js)
		if not os.path.exists(self.css):
			os.makedirs(self.css)

	def download_page(self):
		'''download page by urllib2
		'''
		try:
			request = urllib2.Request(self.url)
			request.add_header('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) \
			    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36')
			response = urllib2.urlopen(request)
			self.page = response.read()
			return 1
		except Exception, e:
			if hasattr(e,"code"):
				print e.code
			if hasattr(e, "reason"):
				print e.reason
			return 0
			
	def para_page(self):
	    '''para the page , get the src to download the css, js, image
		'''
		soup = BeautifulSoup(self.page)
		srcs = soup.find_all(src=True)
		hrefs = soup.find_all(href=True)
		# get every url of img, js, css
		for each_src in srcs:
			print each_src
			if each_src.name == 'img':
				if each_src.has_attr('original'):
					urllib.urlretrieve(each_src['original'],
					    self.img+'/'+each_src['original'].split('/')[-1])
					each_src['src'] = 'img/'+each_src['original'].split('/')[-1]
					each_src['original'] = 'img/'+each_src['original'].split('/')[-1]
				else:
					urllib.urlretrieve(each_src['src'], 
					    self.img+'/'+each_src['src'].split('/')[-1])
					each_src['src'] = 'img/'+each_src['src'].split('/')[-1]
			if each_src['src'].split('.')[-1] == 'js':
				urllib.urlretrieve(each_src['src'], 
				    self.js+'/'+each_src['src'].split('/')[-1])
				each_src['src'] = 'js/'+each_src['src'].split('/')[-1]
			if each_src['src'].split('.')[-1] == 'css':
				urllib.urlretrieve(each_src['src'], 
				    self.css+'/'+each_src['src'].split('/')[-1])
				each_src['src'] = 'css/'+each_src['src'].split('/')[-1]
		# some other js, css, img 
		for each_href in hrefs:
			print each_href
			if each_href['href'].split('.') == 'img':
				urllib.urlretrieve(each_href['href'], 
				    self.img+'/'+each_href['href'].split('/')[-1])
				each_href['href'] = 'img/'+each_href['href'].split('/')[-1]
			if each_href['href'].split('.') == 'js':
				urllib.urlretrieve(each_href['href'], 
				    self.img+'/'+each_href['href'].split('/')[-1])
				each_href['href'] = 'js/'+each_href['href'].split('/')[-1]
			if each_href['href'].split('.') == 'css':
				urllib.urlretrieve(each_href['href'], 
				    self.img+'/'+each_href['href'].split('/')[-1])
				each_href['href'] = 'css/'+each_href['href'].split('/')[-1]
		# save index.html
		with open(self.index+'/index.html', 'w+') as f:
			f.write(str(soup))


def main():
	'''main function: every 60s Backup
	'''
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == '-d':
			d = sys.argv[i+1]
		if sys.argv[i] == '-u':
			url = sys.argv[i+1]
		if sys.argv[i] == '-o':
			path = sys.argv[i+1]
	print d , url, path
	b = Backup(d, url, path)
	# loop to backup
	while True:
		if b.download_page() == 1:
			b.para_page()
		else:
			print "network error!"
		time.sleep(60)

if __name__ == '__main__':
	main()
