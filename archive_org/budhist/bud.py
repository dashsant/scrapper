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


def get_download_metadata(id):
	catalogs = []
	url = "https://archive.org/details/" + id
	head = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
	head["Cookie"] = "logged-in-sig=1571414609+1539878609+rsBi1opFTHa5MoQyTs7tF7kzc%2FQ0VeopRed3FAcE%2BQQ2eJbFZseBUvj2Zonql1dlVGmkrdOKTs2Qb%2BLSwrurAUcuR4damWJD2vP%2FMAWrgnUSwE7s%2BDY1Himg5v6yKWeImliHok3ZJ8Xx1Mp2Hq88pMScpHUlB8oe0iSOt2nOE%2FU%3D; logged-in-user=dashsant%40hotmail.com"
	head["Connection"]="keep-alive"
	req = urllib.request.Request(url , headers=head)
	opn = urllib.request.urlopen(req)
	print(opn.getheader("Set-Cookie"))
	head["Cookie"] = head["Cookie"] + opn.getheader("Set-Cookie")
	urlContent = opn.read()
	#soup = BeautifulSoup(urlContent, "lxml")
	#scripts = soup.find("script")
	urlTexts = urlContent.decode("utf=8")
	lines = urlTexts.split("\n")
	for line in lines:
		if line.find("BookReaderJSIA.php?") >= 0:
			meta_url = line.strip()
			break
	if len(meta_url) > 0:
		a = meta_url.find("'")
		b = meta_url.find("," , a+1)
		meta_url = "https:" + meta_url[a+1:b-1]
		print(meta_url)
	req2 = urllib.request.Request(meta_url , headers=head)
	content = urllib.request.urlopen(req2).read()
	#print(content)
	o = json.loads(content.decode("utf-8"))
	return o["data"],head

def get_image_urls(data):
	leafMap = data["leafMap"]

	imageUrls = []
	for leafNo in leafMap:
		imgStr = str(leafNo);
		for i in range(0, 4 - len(imgStr)):
			imgStr = "0" + imgStr
		insideZipPrefix = data["subPrefix"].split("/")[0]
		imageFormat = data["imageFormat"]
		file = insideZipPrefix + '_' + imageFormat + '/' + insideZipPrefix + '_' + imgStr + '.' + imageFormat;
		
		url = "https://" + data["server"] + '/BookReader/BookReaderImages.php?'
		zipS = "zip="+data["imageStackFile"].replace("\\" , "")
		fileS = "file="+file
		
		url = url + zipS + "&" + fileS
		
		imageUrls.append(url)
		
	return imageUrls

def fetchImages(id, dirName , urls, imageFormat, head):
	tmp = dirName + id + "/"
	print(id)
	print (tmp)
	if not os.path.exists(tmp):
		os.mkdir(tmp)
	pageNo = 1
	for url in urls:
		file_path = tmp + "page-" + str(pageNo) + "." + imageFormat
		pageNo = pageNo + 1
		req = urllib.request.Request(url , headers=head)
		content = urllib.request.urlopen(req).read()
		time.sleep(1)
		with open(file_path , "wb") as f:
			f.write(content)
		
def main():
	# load the file
	# read ids
	#
	f = open("budhist_collection.txt" , "r")
	start = int(sys.argv[1])
	finish = int(sys.argv[2])
	baseFolder = sys.argv[3]
	cnt = 1 

	for id in f:
		id = id.strip()
		if cnt < start:
			continue
		if cnt > finish :
			break
		data , head = get_download_metadata(id)
		imageUrls = get_image_urls(data)
		fetchImages(id , baseFolder , imageUrls , data["imageFormat"], head)
		cnt = cnt + 1

main()
