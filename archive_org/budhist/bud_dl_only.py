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

def get_image_urls(data ):
		
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

def fetchImages(id, dirName , urls, imageFormat, head ):
	pageNo = 1
	files = []
	missing_img = []
	for url in urls:
		file_path = dirName + "page-" + str(pageNo) + "." + imageFormat
		pageNo = pageNo + 1
		try:
			req = urllib.request.Request(url , headers=head)
			content = urllib.request.urlopen(req , None, 10*60).read()
			#time.sleep(1)
			with open(file_path , "wb") as f:
				f.write(content)
			files.append(file_path)
		except:
			missing_img.append(file_path)
			print("Exception for " + file_path)
	with open(dirName +"image_files.json" , "w") as fw:
		json.dump(files , fw)
	if len(missing_img) > 0:
		with open(dirName +"mising_image_files.json" , "w") as fw:
			json.dump(missing_img , fw)
	if len(files) > 0:
		storePDFFiles(files, dirName , id)
		zipCmd = "zip -r " + id + ".zip " + dirName
		subprocess.call(zipCmd , shell=True)
		cmd = "gdrive upload --parent 1-kFLO5bFVCXp1W8KzT8RhJFj0HNPmgC-    " + id + ".zip"
		subprocess.call(cmd , shell=True)
		rmZipFileCmd = "rm " + id + ".zip"
		subprocess.call(rmZipFileCmd  , shell=True)
		cmd = "rm " + dirName + "*."+imageFormat
		subprocess.call(cmd  , shell=True)
		cmd = "rm " + dirName + "*.pdf"
		subprocess.call(cmd  , shell=True)
		

def storePDFFiles(files , dirName , id) :
	noOfParts = int(len(files)/100)
	if (len(files) % 100) > 0:
		noOfParts = noOfParts + 1
	for i in range(1 , noOfParts + 1):
		st = (i-1) * 100
		end = i * 100 
		if(len(files) < end):
			end = len(files)
		pdfImgFileNames = []
		for j in range(st , end):
			pdfImgFileNames.append(files[j])
		print(pdfImgFileNames[len(pdfImgFileNames) -1])
		pdf_bytes = img2pdf.convert(pdfImgFileNames )
		pdfFileName = dirName + id + "-part-"+str(i) + ".pdf"
		print(pdfFileName )
		with open(pdfFileName , "wb") as fpdf:
			fpdf.write(pdf_bytes)
		cmd = "gdrive upload --parent 1-kFLO5bFVCXp1W8KzT8RhJFj0HNPmgC-    " + pdfFileName
		subprocess.call(cmd , shell=True)

def uploadFolders():
	folderName = sys.argv[1]
	id = sys.argv[2]
	fileNames = []
	for file in os.listdir(folderName):
		if file.find(".jp2") > 0:
			fileNames.append(file)
	sortedFileNames = []
	for i in range(1 , len(fileNames) + 1):
		tmp = folderName + "page-" + str(i) + ".jp2"
		if os.path.isfile(tmp):
			sortedFileNames.append(tmp)
	storePDFFiles(sortedFileNames , folderName , id)
	zipCmd = "zip -r " + id + ".zip " + folderName
	subprocess.call(zipCmd , shell=True)
	cmd = "gdrive upload --parent 1-kFLO5bFVCXp1W8KzT8RhJFj0HNPmgC-    " + id + ".zip"
	subprocess.call(cmd , shell=True)
	rmZipFileCmd = "rm " + id + ".zip"
	subprocess.call(rmZipFileCmd  , shell=True)
def getUrlFromBrOptions(o):
	uu = o["data"]
	res = []
	for u in uu:
		for urlInfo in u:
			t = urlInfo["uri"]
			res.append(t.replace("\\" , ""))
	return res
			
def main():
	# load the file
	# read ids
	#
	f = open("budhist_collection.txt" , "r")
	#fmsg = open("scrapper.log" , "w+")
	start = int(sys.argv[1])
	finish = int(sys.argv[2])
	baseFolder = sys.argv[3]
	cnt = 1 

	for id in f:
		id = id.strip()
		if cnt < start:
			cnt = cnt + 1
			continue
		if cnt > finish :
			print("finished all")
			break
		
		cnt = cnt + 1
		data , head  = get_download_metadata(id)
		dirName = baseFolder + id + "/"
		if not os.path.exists(dirName):
			os.mkdir(dirName)
		with open(dirName + id+".json" , "w") as fw:
			json.dump(data ,fw)
		if "isRestricted" in data.keys():
			if data["isRestricted"]:
				#msg = id + " is restricted" + "\n"
				#fmsg.write(msg)
				#fmsg.close()
				#fmsg = open("scrapper.log" , "w+")
				continue
			else:
				try:
					imageUrls = get_image_urls(data  )
					fetchImages(id , dirName , imageUrls , data["imageFormat"], head )
				except:
					print ("Exception in fetching " + id)
					continue
		elif "data" in data.keys():
			dt=data["data"]
			if dt["isRestricted"]:
				continue
			else:
				try:
					bro = data["brOptions"]
					imageUrls = getUrlFromBrOptions( bro)
					fetchImages(id , dirName , imageUrls , bro["imageFormat"], head )
				except:
					print ("Exception in fetching " + id)
					continue
				

main()
#uploadFolders()
