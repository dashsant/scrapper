from urllib.parse import urlencode
import urllib.request
import json
from os.path import basename
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
import datetime
import traceback
import time
import sys
import re
import os
import subprocess
import img2pdf


def get_meta_data(keyword):
	u = "https://www.pdfdrive.com/search?q=######&pagecount=&pubyear=&searchin="
	url = u.replace("######" , keyword)

	head = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
	req = urllib.request.Request(url , headers=head)
	opn = urllib.request.urlopen(req)
	urlContent = opn.read()
	soup = BeautifulSoup(urlContent, "lxml")
	r = soup.find("div" , {"id":"result-found"})
	if not r:
		return []
	c = r.find("strong")
	tmp = str(c.contents[0].strip())
	tmp = tmp.replace("," , "")
	count = int(tmp)
	noOfPages = int(count/20)
	if count%20 > 0:
		noOfPages = noOfPages + 1
	metaDiv = soup.find("div" , {"class":"files-new"})
	metas = []
	if not metaDiv:
		print("Meta Not Found : " +  url)
	else:
		metas.extend(getMetaDataFromDiv(metaDiv))

	metas.extend(getMetaDataFromDiv(metaDiv))
	if noOfPages > 1:
		for page in range(2 , noOfPages + 1):
			pageStr = "&page=" + str(page)
			url = u.replace("######" , keyword) + pageStr
			req = urllib.request.Request(url , headers=head)
			opn = urllib.request.urlopen(req)
			urlContent = opn.read()
			metaDiv = soup.find("div" , {"class":"files-new"})
			if not metaDiv:
				print("Meta Not Found : " +  url)
			else:
				metas.extend(getMetaDataFromDiv(metaDiv))
	return metas
			
def getMetaDataFromDiv(metaDiv):
	lis = metaDiv.find_all("li")
	metas = []
	for li in lis:
		meta = {}
		fileR = li.find("div" , {"class":"file-right"})
		if not fileR:
			continue
		t = fileR.find("a")
		h2 = t.find("h2")
		title = "NA"
		if h2:
			title = str(h2.contents[0])
		fileInfo = fileR.find("div" , {"class":"file-info"})
		p = fileInfo.find("span" , {"class" : "fi-pagecount "})
		page = "NA"
		if p:
			page = str(p.contents[0])
			
		y = fileInfo.find("span" , {"class" : "fi-year "})
		year = "NA"
	
		if  y:
			year = str(y.contents[0])
		meta["title"] = title
		meta["page"] = page
		meta["year"] = year
		metas.append(meta)
			
	return metas 

def main():
	f = open("keywords.txt" , "r")
	keywordline = f.read()
	karr = keywordline.split(",")
	for keyword in karr:
		keyword = keyword.strip()
		w = open(keyword+".csv" , "w")
		metas = get_meta_data(keyword)
		for meta in metas:
			line = meta["title"] + "\t" +  meta["page"] + "\t" + meta["year"]	
			w.write(line)
			w.write("\n")
		w.close()
		print("Completed for keywor " + keyword )
	f.close()
	
	
main()
#uploadFolders()
