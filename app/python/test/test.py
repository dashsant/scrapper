# websiteTxtSearcher.py
# Searches a website recursively for any given string.
# FB - 201009105
import urllib.request
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

# recursively search starting from the root URL
def main():
	#initialize database
	try:
		client = MongoClient()
		db = client["news_scraper"]
	except:
		traceback.print_exc()

	f = open("../news_websites.txt" , "r")
	for line in f:
		rUrl = line.strip()
		if is_url_visited(rUrl , db) == True:
			print(rUrl)


	client.close()


def is_url_visited(url , db):
	res = False
	try:
		collection = db["visited_url"]
		if collection.find_one({"_id":url}) is not None:
			res = True
	except:
		logging.getLogger().exception("")	
	return res

def mark_url_visited(url , db):
	if config.url_visited_check == False:
		rerurn
	try:
		collection = db["visited_url"]
		collection.insert_one({"_id":url} , {"visited":"True"})
	except:
		logging.getLogger().exception("")

main()
