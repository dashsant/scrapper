from urllib.parse import urlencode
import urllib.request
import json
from urllib.parse import urlparse
import logging
import datetime
import traceback
import time
import sys
import re
import os
from bs4 import BeautifulSoup
import urllib.request
import json
import os.path
import shutil
import traceback

def get_meta():
	url = "https://dli.sanskritdictionary.com/functions.php?WhichField=mainsearch&Value=Digital%20Library%20Of%20India&Value1=&pageToken=####"
	#url = u.replace("page####" , str(pageNum))
	#url = url.replace("*****" , searchStr)
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.158 Safari/537.36 Vivaldi/2.5.1525.43'}
	token = ""
	try:
		allObj = {}
		i = 0
		while True:
			u = url.replace("####", token)
			req = urllib.request.Request(u , headers=headers)
			print(u)
			opn = urllib.request.urlopen(req)
			urlContent = opn.read()
			soup = BeautifulSoup(urlContent, "lxml")
			tk = soup.find("input" , {"name":"pageToken"})
			token = tk["value"]
			print (token)
			divs = soup.find_all("div" ,  class_="wholediv")
		
			for div in divs:
				obj,id = get_objDetail(div)
				allObj[id] = obj
				#break
			if len(token) < 10:
				break
			i = i + 1
			#if i == 2:
			#	break
		#print(allObj)
		jf = open("details.json" , "w")
		json.dump(allObj , jf)
		jf.close()
	except Exception:
		jf = open("details.json" , "w")
		json.dump(allObj , jf)
		jf.close()
		traceback.print_exc()
		

def get_objDetail(div):
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.158 Safari/537.36 Vivaldi/2.5.1525.43'}

	obj = dict()
	tmp = div.find("a" , href=True)
	href = tmp["href"]
	
	t = href.split("?Id=")
	id = t[1]
	obj["gdr_id"]=id
	u = "https://dli.sanskritdictionary.com/" + href
	obj["src_url"] = u
	obj["pdf_url"] = "https://drive.google.com/uc?export=download&id=" + id
	ureq = urllib.request.Request(u , headers=headers)
	uopn = urllib.request.urlopen(ureq)
	uContent = uopn.read()
	usoup = BeautifulSoup(uContent, "lxml")
	ul = usoup.find("ul" , class_="ul-list")
	metas = ul.find_all("div" , class_="flex-div")
	metaObj=get_mataObj(metas)
	obj["meta"] = metaObj
	return obj , id
	
		
def get_mataObj(allDivs):
	metaObj={}
	for meta in allDivs:
		m = str(meta).split("</span><span>")
		attrib = (m[0].split("<span>"))[1]
		val = (m[1].split("</span></div>"))
		if len(val) > 1:
			val = val[0]
		else:
			val = ""
		metaObj[attrib.replace(":","")]= val	
	return metaObj
	
get_meta()

	
