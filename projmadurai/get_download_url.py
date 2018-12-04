from urllib.parse import urlencode
import urllib.request
import json
from os.path import basename
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
import datetime
import traceback
import pymongo
from pymongo import MongoClient
import time
import sys
import re
import os



def get_download_url():
	catalogs = []
	url = "https://www.projectmadurai.org/pmworks.html"
	req = urllib.request.Request(url , headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
	urlContent = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(urlContent, "lxml")
	table = soup.find("table" , {"id": "sortabletable"})
	tb = table.find("tbody",{})
	rows = tb.find_all("tr" , {})
	pdfFileUrl = {}
	kindleFileUrl={}
	for row in rows:
		cols = row.find_all("td")
		print(type(cols))
		catalog = {}
		idx = 0
		for col in cols:
			if idx == 0:
				catalog["workno"] = str(col.renderContents().decode("utf-8"))
			if idx == 1:
				catalog["title"] =  str(col.renderContents().decode("utf-8"))
			if idx == 2:
				catalog["author"] = str(col.renderContents().decode("utf-8"))
			if idx == 3:
				catalog["genre"] = str(col.renderContents().decode("utf-8"))
			if idx == 4:
				links = col.find_all("a")
				fileNames = []
				for link in links:
					try:
						href = str(link['href'])
						linkText = str(link.renderContents().decode("utf-8"))
						fileNames.append(str(linkText))
						pdfFileUrl[linkText] = "https://www.projectmadurai.org"+href
					except Exception as e:
						pass
				catalog["pdfs"] = fileNames
			if idx == 5:
				unicodeHtmlLinks = []
				links = col.find_all("a")
				for link in links:
					try:
						href = str(link['href'])
						fullHref = "https://www.projectmadurai.org"+href
						unicodeHtmlLinks.append(str(fullHref))
					except Exception as e:
						pass
				catalog["unicodeHtml"] = unicodeHtmlLinks
			if idx == 6:
				links = col.find_all("a")
				kindleFiles = []
				for link in links:
					try:
						href = str(link['href'])
						linkText = link.renderContents().decode("utf-8")
						kindleFiles.append(str(linkText))
						kindleFileUrl[str(linkText)] = "https://www.projectmadurai.org"+href
					except Exception as e:
						pass
				catalog["kindleFiles"] = kindleFiles
			idx = idx + 1
		print(catalog)
		catalogs.append(catalog)
	with open('proj_madurai_meta.json', 'w') as fp:
		json.dump(catalogs , fp)

get_download_url()	
