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
import subprocess

def download_file(url , fn):
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.158 Safari/537.36 Vivaldi/2.5.1525.43'}
	headers["Accept-Encoding"] = "identity;q=1, *;q=0"
	headers["chrome-proxy"] = "frfr"
	headers["Range"] = "bytes=0-"
	headers["Accept-Encoding"] = "identity;q=1, *;q=0"
	headers["Referer"] = "http://ncaa.gov.in/repository/search/"

	#url = "http://ncaa.gov.in//vol1/ncaa-archive-data//Cultural_AIP_Record/NAI/NAI-001-FR/NAI-001-FR_main/Video/MP4/NAI-001-FR.mp4";
	#url = "http://ncaa.gov.in//vol1/ncaa-archive-data//Portal_Record/NSS/NSS-ACC_12902_VC_288_NSS_DIGN_65-VHS.mp4"
	req = urllib.request.Request(url , headers=headers)
	opn = urllib.request.urlopen(req)
	urlContent = opn.read()
	#fn = "NSS-ACC_12902_VC_288_NSS_DIGN_65-VHS.mp4"
	with open(fn , "wb" )as file:
		file.write(urlContent)
		
#Directory 1qRCGA6YEZ5ZukcN5W-79e16-LO85QVg2 created
#1qRCGA6YEZ5ZukcN5W-79e16-LO85QVg2
#gdrive list --query " '1qRCGA6YEZ5ZukcN5W-79e16-LO85QVg2' in parents"
def upload():
	with open("ncaa_meta_a_82.json" , "r") as jf:
		persistedMetaObj = json.load(jf)
	eObj = load_existing_uloads()
	for k,v in persistedMetaObj.items():
		dlUrls = v["downloadUrl"]
		for dl in dlUrls:
			dl = dl.strip()
			tmp = dl.split("/")
			fn = tmp[-1]
			
			if fn in eObj:
				print("File already uploaded - " + fn)
				continue
				
			fn = "C:\\Personal\\ncaa\data\\" + fn
			exec_gd(fn)
			
def load_existing_uloads():
	f = open("C:\\Personal\\ncaa\\gdrive\\out.txt","r")
	obj={}
	for line in f:
		l = line.strip()
		tmp = l.split("\t")
		obj[tmp[1].strip()] = tmp[0].strip()
	f.close()
	return obj
	
def exec_gd(fn):
	cmd = "C:\\gdrive\gdrive upload --parent 1qRCGA6YEZ5ZukcN5W-79e16-LO85QVg2  " + fn
	#cmd = "dir "
	p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
	output = p.stdout.read()
	tmp = str(output)
	gdriveId = ""
	s = tmp.find("Uploaded")
	if s > 0:
		s = tmp.find(" " , s)
		e = tmp.find(" at", s)
		gdriveId = (tmp[s+1:e])
	print(gdriveId)
	return gdriveId
	

def main():
	upload()
	
main()		
#exec_gd("C:\\Personal\\ncaa\\data\\IGRMS-A_544-AC_SIDE_A.mp3")			
