import urllib.request
import json
import urllib.parse
import sys
#from pymongo import MongoClient
import time

apiKey="ba12971186964f16b475bcd4606d0b05"

def get_url(kf , page):
	k = open(kf , "r")
	keywords = ""
	for line in k:
		t = line.strip()
		if len(t) > 0:
			keywords = keywords + t + " OR "
	query = keywords[0:len(keywords)-4]
	tmp = {}
	tmp["q"] = query
	tmp["apiKey"] = apiKey
	tmp["pageSize"] = 100
	tmp["page"] = page
	tmp["from"] = "2018-10-31T01:53:01"
	tmp["to"] = "2018-11-01T01:53:01"
	qstr = urllib.parse.urlencode(tmp)
	k.close()
	url = "https://newsapi.org/v2/everything?" + qstr
	return url

def main():
	if len(sys.argv) < 3 :
		print("Insufficient argument passed")
		print("python scrape_news_api.py <keyword_file> <result_file>")
		return
	else:
		kf = sys.argv[1].strip()
		rf = sys.argv[2].strip()
	try:
		rff = open(rf , "w")
		#client = MongoClient()
		#db = client["news_scraper"]
	except Exception as e:
		print(e)
		return

	url = get_url(kf , 1)
	try:
		req = urllib.request.Request(url)
		urlContent = urllib.request.urlopen(req).read()
	except Exception as e:
		print(e)
		return
	
	o = json.loads(urlContent)
	cnt = int(o["totalResults"])
	print(cnt)
	aticles = o["articles"]
	for art in aticles:
		try:
			line = art["title"] + "," + art["url"]
			rff.write(line)
			rff.write("\n")
			#art["_id"] = art["url"]
			#db["news_api_1"].insert( art)
		except Exception as e:
			print(e)
			pass

	pagecnt = int(cnt/100)
	if cnt%100 > 0:
		pagecnt = pagecnt + 1

	sleepSeed = 1
	for p in range(2 , pagecnt + 1):
		#time.sleep(60*sleepSeed)
		url = get_url(kf , p)
		try:
			req = urllib.request.Request(url)
			urlContent = urllib.request.urlopen(req).read()
			o = json.loads(urlContent)
			aticles = o["articles"]
			for art in aticles:
				try:
					line = art["title"] + "," + art["url"]
					rff.write(line)
					rff.write("\n")
					#art["_id"] = art["url"]
					#db["news_api_1"].insert( art)
				except Exception as e:
					print(e)
					pass
		except  Exception as e:
			sleepSeed = sleepSeed*2
			print(e)
			pass
	rff.close()

 
main()	
