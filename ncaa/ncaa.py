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

def get_urls(searchStr , pageNum , persistedMetaObj):
	u = "http://ncaa.gov.in/repository/search/retriveBasicSearchResult/page####/10?_exactWordSearch=on&searchString=*****&metadataSearchType=Metadata&mediumName="
	url = u.replace("page####" , str(pageNum))
	url = url.replace("*****" , searchStr)
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.158 Safari/537.36 Vivaldi/2.5.1525.43'}
	headers["Accept-Encoding"] = "identity;q=1, *;q=0"
	headers["chrome-proxy"] = "frfr"
	headers["Range"] = "bytes=0-"
	headers["Accept-Encoding"] = "identity;q=1, *;q=0"

	req = urllib.request.Request(url , headers=headers)
	opn = urllib.request.urlopen(req)
	urlContent = opn.read()
	soup = BeautifulSoup(urlContent, "lxml")
	divs = soup.find_all("div" ,  class_="bg_grad")
	objArr = []
	for d in divs:
		obj = dict()
		tmp = d.find("div" , class_="boxshadow_s")
		hrefD = tmp.find("a", href=True)
		dataUrl = "http://ncaa.gov.in"+ hrefD['href']
		if dataUrl in persistedMetaObj:
			continue
		obj["url"] = dataUrl
		dataReq = urllib.request.Request(dataUrl , headers=headers)
		dataOpn = urllib.request.urlopen(dataReq)
		dataContent = dataOpn.read()
		datasoup = BeautifulSoup(dataContent, "lxml")
		script = datasoup.find("script" , {"language":"JavaScript"})
		strS = str(script)
		s = strS.find("var metadata=")
		s = strS.find("{" , s)
		e = strS.find("};" , s)
		metadata = strS[s:e+1]
		metaObj = json.loads(metadata)
		s = strS.find("var previewFilePathList")
		s = strS.find("=" , s)
		e = strS.find('";',s)
		filePathStr = strS[s+3:e-1]
		files = filePathStr.split(",")
		obj["metadata"] = metaObj
		obj["downloadUrl"] = files
		objArr.append(obj)
		persistedMetaObj[dataUrl] = obj
	return objArr

def get_result_cnt(searchStr ):
	u = "http://ncaa.gov.in/repository/search/retriveBasicSearchResult/1/10?_exactWordSearch=on&searchString=****&metadataSearchType=Metadata&mediumName="
	url = u.replace("****" , searchStr)
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.158 Safari/537.36 Vivaldi/2.5.1525.43'}
	headers["Accept-Encoding"] = "identity;q=1, *;q=0"
	headers["chrome-proxy"] = "frfr"
	headers["Range"] = "bytes=0-"
	headers["Accept-Encoding"] = "identity;q=1, *;q=0"

	req = urllib.request.Request(url , headers=headers)
	opn = urllib.request.urlopen(req)
	urlContent = opn.read()
	strUrlContent = str(urlContent)
	s = strUrlContent.find("Total Search")
	if s < 0:
		totalCount = 0
	else:
		s = strUrlContent.find("(" , s)
		e = strUrlContent.find(")" , s)
		totalCount = strUrlContent[s+1:e]
		
	return int(totalCount)


def main():
	if len(sys.argv) < 2:
		print("Please enter the search string")
		
	searchStr = sys.argv[1]
	resultCnt = get_result_cnt(searchStr)
	print(resultCnt)
	if os.path.isfile("meta.json"):
		with open("meta.json" , "r") as jf:
			persistedMetaObj = json.load(jf)
			shutil.copy("meta.json" , "meta.json.bak")
	else:
		persistedMetaObj = {}
	print(len(persistedMetaObj.keys()))
	cnt = get_result_cnt(searchStr)
	pageCnt = int(cnt/10)
	if cnt%10:
		pageCnt = pageCnt+1
	for page in range(1, pageCnt+1):
		objs = get_urls(searchStr , page , persistedMetaObj)
		print("Completed collecting meta information for " + str(page))
		fn = "ncaa_meta_" + searchStr
		fn = fn+"_"+str(page)+".json"
		f = open( fn , "w")
		json.dump(persistedMetaObj , f)
		f.close()
	
	jf = open("meta.json" , "w")
	json.dump(persistedMetaObj , jf)
	jf.close()



def merge():
	obj = {}
	baseDir = "C:\\Personal\\ncaa\\merge"
	files = os.listdir(baseDir)
	print(files)
	for f in files:
		print(f)
		fn = baseDir + "\\"+f
		t = open(fn , "r")
		jo = json.load(t)
		t.close()
		for i,v in jo.items():
			obj[i] = v
			
	print(len(obj.keys()))
	fw = open("meta.json" , "w")
	json.dump(obj , fw)
	fw.close()

main()	
#merge()
