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
	c = r.find("strong")
	count = int(c.renderContent())
	print(count)
	noOfPages = int(count/20)
	if count%20 > 0:
		noOfPages = noOfPages + 1
	metaDiv = soud.find("div" , {"class":"files-new"})
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
			metaDiv = soud.find("div" , {"class":"files-new"})
			if not metaDiv:
				print("Meta Not Found : " +  url)
			else:
				metas.extend(getMetaDataFromDiv(metaDiv))
			
def getMetaDataFromDiv(metaDiv):
	lis = metaDiv.find_all("li")
	metas = []
	for li in lis:
		meta = {}
		fileR = li.find("div" , {"class":"file-right"})
		t = fileR.find("a")
		title = "NA"
		if not t:
			title = t.renderContent()
		fileInfo = fileR.find("div" , {"class":"file-info"})
		p = fileInfo.find("span" , {"class" : "fi-pagecount "})
		page = "NA"
		if not p:
			page = p.renderContent()
		y = fileInfo.find("span" , {"class" : "fi-year "})
		year = "NA"
		if not y:
			year = y.renderContent()
		meta["title"] = title
		meta["page"] = page
		meta["year"] = year
		metas.append(meta)
	return metas

def main():
	f = open("keywords.txt" , "r")
	w = open("metas.csv" , "w")
	for keyword in f:
		metas = get_meta_data(keyword)
		for meta in metas:

	f.close()
	w.close()
	
	
main()
#uploadFolders()
