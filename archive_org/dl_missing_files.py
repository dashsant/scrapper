from os.path import basename
import datetime
import traceback
import time
import sys
import re
import os
import subprocess
import string

def download_file(download_url , file_path):
	headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}

		
	url = "https://archive.org"+ string.strip(download_url)
	print(url , file_path)
	try:
		c = "wget " + url + " -O   " + file_path
		print(c)
		subprocess.call(c , shell=True)
		return True
	except Exception as e:
		pass
	return False
	

def main():
	if len(sys.argv) < 3:
		print("Please enter start and finish")
		return
	start = int(sys.argv[1])
	finish = int(sys.argv[2])
	data_out_folder = "/root/archive_download/missing" + str(start) + "/" 
	if not os.path.exists(data_out_folder):
    		os.makedirs(data_out_folder)
	f = open('missing_files.txt' , 'r')
	download_count = 0
	for line in f:
		download_count = download_count + 1
		if download_count < start:
			continue
		
		download_url = line
		name  = get_downoad_file_path(download_url)
		path = data_out_folder + name

		if download_file(download_url , path) == True:
			pass
		else:
			print("Download of the file failed " + id)
		if download_count == finish:
			break
	f.close()


def get_downoad_file_path(url):
	t = url
	if(t.find("/download/") == 0):
		t = t[10:]
	t = t[0:-4]
	regx = re.compile('[./%&$#]')
	t = regx.sub("_" , t)
	t = t + ".pdf"
	return t
	
main()
