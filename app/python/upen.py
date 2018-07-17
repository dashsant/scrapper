import urllib.request
import os
from os.path import basename
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
import datetime
import traceback
import json
import pymongo
from pymongo import MongoClient
import time
import sys
import config
import re
import subprocess

def get_meta_info(u):
	req = urllib.request.Request(u , headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
	urlContent = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(urlContent, "lxml")
	tables = soup.find_all("div" , {"id":"recordinfo"})
	metainfo = {}
	if len(tables) == 0:
		return metainfo
	table = tables[0].find("table")
	rows = table.find_all("tr")
	for row in rows:
		cols = row.find_all("td")
		if len(cols) >= 2:
			metainfo[cols[0].text] = cols[1].text
	print(metainfo)
	return metainfo

def download_file(url , file_path):
	headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
	cmd = "wget " + url + " -O " +file_path
	print(cmd)
	try:
		urllib.request.urlretrieve(url , file_path)
		#subprocess.call(cmd , shell=True)
		return True
	except Exception as e:
		pass
	return False

def main():
	startIdx = sys.argv[1]
	outf = "/home/archive_download/upen/"#sys.argv[1]
	url = "http://dla.library.upenn.edu/dla/medren/search.html?rows=100&fq=language_facet%3A%22Sanskrit%22&start=" + startIdx
	srcUrl = "http://dla.library.upenn.edu/dla/medren/"
	req = urllib.request.Request(url , headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
	urlContent = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(urlContent, "lxml")
	titles = soup.find_all("div" , {"class": "medrenresultstitle"})
	mss = []
	for title in titles:
		o = {}
		atag = title.find("a")
		href = atag["href"]
		idstart = href.find("id=")
		metaurl = "http://dla.library.upenn.edu/dla/medren/record.html?" + href[idstart:]
		metaObj = get_meta_info(metaurl)
		pageUrl = srcUrl + href
		req1 = urllib.request.Request(pageUrl , headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
		urlContent1 = urllib.request.urlopen(req1).read()
		soup1 = BeautifulSoup(urlContent1, "lxml")
		imgs = soup1.find_all("img" ,  {"id": "main_image"})
		page_num = 1
		pages = []
		while len(imgs) > 0:
			imgSrc = imgs[0]["src"]
			pages.append(imgSrc)
			page_num = page_num + 1
			pageUrl =  srcUrl + href + "currentpage=" + str(page_num)
			req1 = urllib.request.Request(pageUrl , headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
			urlContent1 = urllib.request.urlopen(req1).read()
			soup1 = BeautifulSoup(urlContent1, "lxml")
			imgs = soup1.find_all("img" ,  {"id": "main_image"})

		o["title"] = atag.text
		o["pages"] = pages
		o["metainfo"] = metaObj
		mss.append(o)
		fp = outf+o["title"]
		if not os.path.exists(fp):
			os.mkdir(fp)
		elif not  os.path.exists(outf+o["title"]+"/moreA"):
			fp = outf+o["title"]+"/moreA"
			os.mkdir(fp)
		elif not  os.path.exists(outf+o["title"]+"/moreB"):
			fp = outf+o["title"]+"/moreB"
			os.mkdir(fp)
		elif not  os.path.exists(outf+o["title"]+"/moreC"):
			fp = outf+o["title"]+"/moreC"
			os.mkdir(fp)
		elif not  os.path.exists(outf+o["title"]+"/moreD"):
			fp = outf+o["title"]+"/moreD"
			os.mkdir(fp)
		elif not  os.path.exists(outf+o["title"]+"/moreE"):
			fp = outf+o["title"]+"/moreE"
			os.mkdir(fp)
		elif not  os.path.exists(outf+o["title"]+"/moreF"):
			fp = outf+o["title"]+"/moreF"
		os.mkdir(fp)


		cnt = 1
		for p in pages:
			download_file(p , fp+"/page_" + str(cnt)+".jpg")
			cnt = cnt + 1
		metaF = open(fp + "/meta.json" , "w")
		json.dump(metaObj, metaF)
			
	fdn = open(outf+"upen_"+startIdx , "w")
	json.dump(mss, fdn)
		
	

main()
