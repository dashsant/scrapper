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


def get_req_header():
	url = "https://archive.org/details/bdrc-W1KG5905"
	head = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
	head["Cookie"] = "logged-in-sig=1571414609+1539878609+rsBi1opFTHa5MoQyTs7tF7kzc%2FQ0VeopRed3FAcE%2BQQ2eJbFZseBUvj2Zonql1dlVGmkrdOKTs2Qb%2BLSwrurAUcuR4damWJD2vP%2FMAWrgnUSwE7s%2BDY1Himg5v6yKWeImliHok3ZJ8Xx1Mp2Hq88pMScpHUlB8oe0iSOt2nOE%2FU%3D; logged-in-user=dashsant%40hotmail.com"
	head["Connection"]="keep-alive"
	req = urllib.request.Request(url , headers=head)
	opn = urllib.request.urlopen(req)
	head["Cookie"] = head["Cookie"] + opn.getheader("Set-Cookie")
	return head


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



def parse(fn):
	result= {}
	f = open(fn)
	cnt = 1
	for line in f:
		if cnt == 1:
			cnt = cnt + 1
			continue
		cnt = cnt + 1
		tmp = line.split()
		if tmp[1].find("-part") > 0:
			key = tmp[1][:tmp[1].find("-part")]
			v = result.get(key , None)
			if v is None:
				v={}
				v["splitPdf"] = [tmp[1]+"####"+tmp[0]]
				result[key] = v
			else:
				s = v.get("splitPdf" , None)
				if s is None:
					s=[tmp[1]+"####"+tmp[0]]
					v["splitPdf"] = s
				else:
					s.append(tmp[1]+"####"+tmp[0])
		elif tmp[1].find(".zip") > 0:
			key = tmp[1][:tmp[1].find(".zip")]
			v = result.get(key , None)
			if v is None:
				v={}
				v["zip"]=tmp[1]
				v["zipDriveId"] = tmp[0]
				result[key] = v
			else:
				v["zip"] = tmp[1]
				v["zipDriveId"] = tmp[0]
		elif tmp[1].find(".pdf") > 0:
			key = tmp[1][:tmp[1].find(".pdf")]
			v = result.get(key , None)
			if v is None:
				v={}
				v["pdf"]=tmp[1]
				v["pdfDriveId"] = tmp[0]
				result[key] = v
			else:
				v["pdf"]=tmp[1]
	return result

def get_missing_files(folderName , id , head):
	file_missing = False
	fn = folderName + id + ".json"
	with open(fn , "r") as f:
		data = json.load(f)	
	urls = get_image_urls(data)
	pageNo = 1
	for url in urls:
		file_path = folderName + "page-" + str(pageNo) + ".jp2"# + imageFormat
		pageNo = pageNo + 1
		if not os.path.isfile(file_path):
			file_missing = True
			print(url , file_path)
			req = urllib.request.Request(url , headers=head)
			content = urllib.request.urlopen(req , timeout=10*60).read()
			with open(file_path , "wb") as f:
				f.write(content)
	return file_missing

def storePDFFiles( folderName , id ) :
	fileNames = []
	for file in os.listdir(folderName):
		if file.find(".jp2") > 0:
			fileNames.append(file)
	files = []
	for i in range(1 , len(fileNames) + 1):
		tmp = folderName + "page-" + str(i) + ".jp2"
		if os.path.isfile(tmp):
			files.append(tmp)
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
		print(pdfImgFileNames[0] , pdfImgFileNames[len(pdfImgFileNames) -1])
		pdf_bytes = img2pdf.convert(pdfImgFileNames )
		pdfFileName = folderName + id + "-part-"+str(i) + ".pdf"
		print(pdfFileName )
		with open(pdfFileName , "wb") as fpdf:
			fpdf.write(pdf_bytes)
		cmd = "gdrive upload --parent 1iRJtGw4X-hT-PB7oR9khW270KqIqLC-1    " + pdfFileName
		subprocess.call(cmd , shell=True)

def replaceZip(folderName , id , gid):
	zipCmd = "zip -r " + id + ".zip " + folderName
	subprocess.call(zipCmd , shell=True)
	#remove the old zip fil
	if  gid:
		cmd = "gdrive delete     " + gid
		subprocess.call(cmd , shell=True)
	cmd = "gdrive upload --parent 1iRJtGw4X-hT-PB7oR9khW270KqIqLC-1    " + id + ".zip"
	subprocess.call(cmd , shell=True)
	rmZipFileCmd = "rm " + id + ".zip"
	subprocess.call(rmZipFileCmd  , shell=True)
def getFoldersWithNoZip(res , baseF):
	fns = os.listdir(baseF)
	cnt = 1 
	cnt_ab = 1
	for fn in fns:
		tmp = res.get(fn , None)
		if tmp is not None:
			c = tmp.get("zipDriveId" , None)
			if not c:
				cnt = cnt +1
				print(tmp)
			a = tmp.get("splitPdf" , None)
			b = tmp.get("pdf" , None)
			if (not a) and (not b) :
				cnt_ab = cnt_ab + 1
			elif c:
				t = baseF + fn
				cmd = "rm -rf " + t
				#print(cmd)
				#subprocess.call(cmd,shell = True)
			
	print(cnt , cnt_ab)

def removeUpload(id,res):
	data = res.get(id)
	a = data["splitPdf"]
	b = data["zipDriveId"]
	for i in a:
		t = i.split("####")
		cmd = "gdrive delete " + t[1]
		print(cmd)
		subprocess.call(cmd , shell=True)
	cmd = "gdrive delete " +b
	print(cmd)
	subprocess.call(cmd , shell=True)
	

def main():
	head = get_req_header()	
	res = parse("/home/santi_dash_gmail_com/scrapper/archive_org/budhist/uploaded_files.txt")
	print(len(res.keys()))
	return
	uploadedEntries = res.keys()
	baseF = "/mnt/disks/budha/data/"
	fns = os.listdir(baseF)
	#getFoldersWithNoZip(res , baseF)
	#return
	#removeUpload( "bdrc-W1CZ888" , res)
	#return

	for fn in fns:
		tmp = res.get(fn , None)
		if tmp is not None:
			idfn = baseF + fn + "/"
			if get_missing_files(idfn , fn , head):
				#re import zip file 
				replaceZip(idfn,fn,tmp["zipDriveId"])
				pass
			c = tmp.get("zipDriveId" , None)
			if not c:
				print("missing zip for fn " + fn)
				replaceZip(idfn,fn,None)
			
			a = tmp.get("splitPdf" , None)
			b = tmp.get("pdf" , None)
			if (not a) and (not b) :
				print (fn)
				storePDFFiles( idfn , fn )					
				pass
			
			#cmd = "rm -rf " + "/home/archive_download/budhist_data/" + fn
			#print(cmd)
			#subprocess.call(cmd, shell=True)

main()
