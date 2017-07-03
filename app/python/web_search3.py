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
import config
import re

# recursively search starting from the root URL
def searchUrl(url, level, keywords, rootUrl , urlListProbed , document , db): # the root URL is level 0
    # do not go to other websites
	o = urlparse(url)
	logging.getLogger().info(o.geturl())
	if  o.netloc.find(rootUrl) < 0:
		return

	if url in urlListProbed: # prevent using the same URL again
		return

	try:
		urlListProbed.append(url)
		if is_url_visited(url , db) == False:
			req = urllib.request.Request(url , headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
			urlContent = urllib.request.urlopen(req).read()
		else:
			print("url already visited : " + o.geturl())
			return

	except Exception as e:
		logging.getLogger().exception(o.geturl())
		return

	soup = BeautifulSoup(urlContent, "lxml")
	
	# remove script tags
	c = soup.find_all('script')
	for i in c:
		i.extract() 

	result = None
	if rootUrl == 'indianexpress.com':
		result = searchIndianExpress(soup , keywords )
	elif rootUrl == 'www.thehindu.com':
		result = searchTheHindu(soup , keywords )
	elif rootUrl == 'timesofindia.indiatimes.com':
		result = searchTOI(soup , keywords)
	elif rootUrl == 'www.aninews.in':
		result = searchANINews(soup , keywords)
	elif rootUrl == 'www.newindianexpress.com':
		result = searchNewindianexpress(soup , keywords)
	elif rootUrl == 'zeenews.india.com':
		result = searchZeeNews(soup , keywords)
	elif rootUrl.find('dnaindia.com') >=0 :
		result = searchDNAIndia(soup , keywords)
	elif rootUrl == 'www.sundayguardianlive.com':
		result = searchSundayGuardin(soup , keywords)
	elif rootUrl == 'www.hindustantimes.com':
		result = searchHindustanTimes(soup , keywords)
	elif rootUrl == 'www.theguardian.com':
		result = searchTheGuardian(soup , keywords)
	elif rootUrl == 'www.ndtv.com':
		result = searchNDTV(soup , keywords)
	elif rootUrl == 'www.mid-day.com':
		result = searchMidDay(soup , keywords)
	elif rootUrl == 'www.news18.com':
		result = searchNews18(soup , keywords)
	elif rootUrl == 'www.opindia.com':
		result = searchOpIndia(soup , keywords)
	elif rootUrl == 'www.livemint.com':
		result = searchLiveMint(soup , keywords)
	elif rootUrl == 'www.sirfnews.com':
		result = searchSirfNews(soup , keywords)
	elif rootUrl.find('in.reuters.com') >= 0:
		result = searchReuters(soup , keywords)
	elif rootUrl.find('swarajyamag.com') >= 0:
		result = searchSwarajya(soup , keywords)
	elif rootUrl == 'currentriggers.com':
		result = searchCurrentRiggers(soup , keywords)
	elif rootUrl == 'satyavijayi.com':
		result = searchSatyaVijayi(soup , keywords)
	elif rootUrl == 'www.hindupost.in':
		result = searchHinduPost(soup , keywords)
	elif rootUrl.find('simplecapacity.com') >= 0:
		result = searchSimpleCapacity(soup , keywords)
	elif rootUrl == 'www.worldreligionnews.com':
		result = searchWorldReligionNews(soup , keywords)
	elif rootUrl == 'worldhindunews.com':
		result = searchWorldHinduNews(soup , keywords)
	elif rootUrl == 'www.dailyo.in':
		result = searchDailyo(soup , keywords)
	elif rootUrl == 'www.avenuemail.in':
		result = searchAvenuemaol(soup , keywords)
	elif rootUrl == 'hinduexistence.org':
		result = searchHinduExistence(soup , keywords)
	elif rootUrl == 'www.hinduhumanrights.info':
		result = searchHinduHumanRights(soup , keywords)
	elif rootUrl == 'www.hindujagruti.org':
		result = searchHinduJagruti(soup , keywords)
	elif rootUrl == 'www.mediacrooks.com':
		result = searchMediaCrooks(soup , keywords)
	elif rootUrl == 'deccanherald.com':
		result = searchDeccanHerald(soup , keywords)	
	elif rootUrl == 'deccanchronicle.com':
		result = searchDeccanChronicle(soup , keywords)	
	elif rootUrl == 'business-standard.com':
		result = searchBusinessStandard(soup , keywords)
	elif rootUrl.find('thehindubusinessline.com') >=0 :
		result = searchHinduBusinessLine(soup , keywords)	
	elif rootUrl == 'telegraphindia.com':
		result = searchTelegraph(soup , keywords)	
	elif rootUrl == 'economictimes.indiatimes.com':
		result = searchEconomicTimes(soup , keywords)
	elif rootUrl == 'www.firstpost.com':
		result = searchFirstPost(soup , keywords)
	elif rootUrl == 'dailypost.in':
		result = searchDailyPost(soup , keywords)
	elif rootUrl == 'bangaloremirror.com':
		result = searchBangaloreMirror(soup , keywords)
	elif rootUrl == 'tribuneindia.com':
		result = searchTribuneIndia(soup , keywords)
	elif rootUrl == 'asianage.com':
		result = searchAsianAge(soup , keywords)
	elif rootUrl == 'scroll.in':
		result = searchScroll(soup , keywords)
	elif rootUrl == 'telanganatoday.com':
		result = searchTelanganaToday(soup , keywords)
	elif rootUrl == 'www.thebetterindia.com':
		result = searchBetterIndia(soup , keywords)
	elif rootUrl == 'financialexpress.com':
		result = searchFinancialExpress(soup , keywords)
	elif rootUrl == 'freepressjournal.in':
		result = searchFreePressJournal(soup , keywords)
	elif rootUrl == 'www.greaterkashmir.com':
		result = searchGreaterKashmirJournal(soup , keywords)
	elif rootUrl == 'mumbaimirror.com':
		result = searchMumbaiMirror(soup , keywords)
	elif rootUrl == 'www.nagalandpost.com':
		result = searchNagalandPost(soup , keywords)
	elif rootUrl == 'www.dailypioneer.com':
		result = searchDailyPioneer(soup , keywords)
	elif rootUrl == 'news.statetimes.in':
		result = searchStateTimes(soup , keywords)
	elif rootUrl == 'www.starofmysore.com':
		result = searchStarOfMysore(soup , keywords)
	elif rootUrl == 'www.navhindtimes.in':
		result = searchNacHindTimes(soup , keywords)
	elif rootUrl == 'morungexpress.com':
		result = searchMorungExpress(soup , keywords)	
	elif rootUrl == 'newstodaynet.com':
		result = searchNewsTodayNet(soup , keywords)	
	elif rootUrl == 'theshillongtimes.com':
		result = searchTheShillongTimes(soup , keywords)	
	elif rootUrl == 'www.newsgram.com':
		result = searchNewsGram(soup , keywords)
	elif rootUrl == 'www.pacifiermedia.com':
		result = searchPacificMedia(soup , keywords)
	elif rootUrl == 'www.haindavakeralam.com':
		result = searchHaindavakeralam(soup , keywords)
	elif rootUrl == 'says.com':
		result = searchSays(soup , keywords)
	elif rootUrl == 'www.chakranews.com':
		result = searchChakraNews(soup , keywords)
	elif rootUrl == 'www.mysteryofindia.com':
		result = searchMysteryOfIndia(soup , keywords)
	elif rootUrl == 'dharmatoday.com':
		result = searchDharmaToday(soup , keywords)
	elif rootUrl == 'postcard.news':
		result = searchPostcardNews(soup , keywords)
	else:
		print("This speicific Site is yet to be implemented " + rootUrl)	
		return
	
	#"." is not a valid for field name in mongo
	key = rootUrl.replace("." , "_")
	# Check if the key for this rootUrl exist
	if key not in document:
		siteDetail = {}
		siteDetail["key_match_count"] = 0
		siteDetail["tag_match_count"] = 0
		siteDetail["children"] = []
		document[key] = siteDetail
	else:
		siteDetail = document[key]

	if result["tag_match"] == True:
		siteDetail["tag_match_count"] = siteDetail["tag_match_count"] + 1
		#Only mark the URL's as visited if there is a tag match. This is to avoid the scenaatio of skipping
		# the main website for every successive run
		mark_url_visited(url , db)
	
	if result["keyword_match"] == True:
		log_result(url)
		siteDetail["key_match_count"] = siteDetail["key_match_count"] + 1 
		urlDetail = {}
		urlDetail["link"] = url
		urlDetail["headline"] = result["headline"]
		urlDetail["author"] = result["author"]
		siteDetail["children"].append(urlDetail)
			
    # if there are links on the webpage then recursively repeat
	if level > 0:
		linkTags = soup.find_all('a')
		if len(linkTags) > 0:
			for linkTag in linkTags:
				try:
					linkUrl = linkTag['href']
					if linkUrl.startswith("http") == False:
						if linkUrl[0] == '/':
							linkUrl = o.scheme + "://" + rootUrl + linkUrl
						else:
							linkUrl = o.scheme + "://" + rootUrl +"/"+ linkUrl
					searchUrl(linkUrl, level - 1, keywords , rootUrl , urlListProbed , document , db)
				except:
					pass

def searchIndianExpress(soup , keywords):
	result = init_result()
	try:
		schema = soup.find("html" , itemtype='http://schema.org/Article')
		headlines = soup.find_all("h1" , itemprop="headline")
		if schema is not None and len(headlines) == 1:
			result["tag_match"] = True
			if(genSearchParagraph(soup.find_all("p") , keywords) is not None):
				result["keyword_match"] = True
				result["headline"] = headlines[0].get_text()
				author = soup.find_all("div" , class_="editor")
				result["author"] = author[0].get_text()
				result["author"] = result["author"].replace("\n" , " ")
				result["author"] = result["author"].replace("\t" , "")
	except:
		logging.getLogger().exception("")
	return result
	
def searchTheHindu(soup , keywords):
	result = init_result()
	try:
		t = soup.find("div",class_="article-topics-container")
		if t is not None:
			result["tag_match"] = True
		paragraphs = soup.find_all("p")
		for p in paragraphs:
			if len(p.attrs) > 0:
				continue
			for searchText in keywords:
				if(p.get_text().find(searchText)) > -1 :
					result["keyword_match"] = True
					return result
	except:
		logging.getLogger().exception("")
	return result
				
def searchTOI(soup , keywords):
	result = init_result()
	try:
		schema = soup.find("html" , itemtype='https://schema.org/NewsArticle')
		if schema is not None:
			result["tag_match"] = True
			content_text = (soup.find("div" ,  itemprop="articleBody")).get_text()
			for searchText in keywords:
				if(content_text.find(searchText)) > -1 :
					result["keyword_match"] = True
					break
	except:
		logging.getLogger().exception("")
	return result

def searchANINews(soup , keywords):
	result = init_result()
	try:
		art = soup.find("article")
		if art is not None:
			result["tag_match"] = True
			content_text = art.get_text()
			for searchText in keywords:
				if(content_text.find(searchText)) > -1 :
					result["keyword_match"] = True
	except:
		logging.getLogger().exception("")
	return result
	
def searchNewindianexpress(soup , keywords):
	return searchPage1(soup , keywords , "article" , {})

def searchPage(soup , keywords , elementTag , filters , lengthCheck=None):
	result = init_result()
	try:
		if isinstance(filters , dict) :
			content = soup.find_all(elementTag , filters)
		elif isinstance(filters , str) :
			content = soup.select(filters)
		if lengthCheck is None and len(content) != 0:
			result["tag_match"] = True
		elif len(content) == lengthCheck:
			result["tag_match"] = True
		if result["tag_match"] == True:
			paragraphs = content[0].find_all("p")
			if genSearchParagraph(paragraphs , keywords) is not None:
				result["keyword_match"] = True
	except:
		logging.getLogger().exception("")
	s = "elementTag: " + str(elementTag) + " filters: " + str(filters) + " lengthCheck:" + str(lengthCheck)
	logging.getLogger().info(s)
	return result

# Does not get the paragraph, rather searches the elements itself
def searchPage1(soup , keywords , elementTag , filters):
	result = init_result()
	try:
		if isinstance(filters , dict) :
			content = soup.find_all(elementTag , filters)
		elif isinstance(filters , str) :
			content = soup.select(filters)
		if len(content) != 0 :
			result["tag_match"] = True
			if genSearchParagraph(content , keywords) is not None:
				result["keyword_match"] = True
	except:
		logging.getLogger().exception("")
	return result

def searchPage2(soup , keywords , elementTag , filters , paragraphFilterText):
	result = init_result()
	s = "elementTag: " + str(elementTag) + " filters: " + str(filters) + " paragraphFilterText:" + str(paragraphFilterText)
	logging.getLogger().info(s)

	try:
		if isinstance(filters , dict) :
			content = soup.find_all(elementTag , filters)
		elif isinstance(filters , str) :
			content = soup.select(filters)
		if len(content) != 0 :
			result["tag_match"] = True
			paragraphs = content[0].find_all("p")
			paragraphs = filterParagraphs(content[0].find_all("p") , paragraphFilterText)
			if genSearchParagraph(paragraphs , keywords) is not None:
				result["keyword_match"] = True
	except:
		logging.getLogger().exception("")
	return result
	
def searchPage4(soup , keywords , elementTag , filters ):
	result = init_result()
	try:
		if isinstance(filters , dict) :
			content = soup.find_all(elementTag , filters)
		elif isinstance(filters , str) :
			content = soup.select(filters)
		if lengthCheck is None and len(content) != 0:
			result["tag_match"] = True
		elif len(content) == lengthCheck:
			result["tag_match"] = True
		if result["tag_match"] == True:
			if genSearchParagraph(content , keywords) is not None:
				result["keyword_match"] = True
	except:
		logging.getLogger().exception("")
	return result
	
def searchZeeNews(soup , keywords):
	return searchPage(soup , keywords , "section" , {"class": 'main-article'})

def searchDNAIndia(soup , keywords):
	return searchPage(soup , keywords , None , {"class": 'article-content'})
	
def searchSundayGuardin(soup , keywords):
	return searchPage(soup , keywords , None , "div.field-content.field-name-body-article")

def searchHindustanTimes(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class": 'story-details' , "itemprop":"articlebody" })

def searchTheGuardian(soup , keywords):
	return searchPage(soup , keywords , "div" , {"itemprop":"articleBody" })
	
def searchNDTV(soup , keywords):
	return searchPage(soup , keywords , "div" , {"itemprop":"articleBody" })

def searchMidDay(soup , keywords):
	return searchPage(soup , keywords , "span" , {"itemprop":"articleBody" })
	
def searchNews18(soup , keywords):
	return searchPage1(soup , keywords , "div" , {"id":"article_body" })
	
def searchOpIndia(soup , keywords):
	return searchPage(soup , keywords , "div" , {"id":"content-main" })

def searchLiveMint(soup , keywords):
	return searchPage(soup , keywords , None , {"id":"main-content" })

def searchSirfNews(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"td-post-content" })

def searchReuters(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":re.compile("PrimaryAsset_container") })

def searchSwarajya(soup , keywords):
	return searchPage(soup , keywords , None , "div.story-element.story-element-text")

def searchCurrentRiggers(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"entry-content" })

def searchSatyaVijayi(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"td-post-content" })

def searchHinduPost(soup , keywords):
	return searchPage2(soup , keywords , "div" , {"id":"main-content" } , "and help pay for our journalism")

def searchSimpleCapacity(soup , keywords):	
	return searchPage2(soup , keywords , "div" , {"id":"content-main" } , "Your email address will not be published")

def searchWorldReligionNews(soup , keywords):
	return searchPage2(soup , keywords , "div" , {"itemprop":"articleBody" , "class":"articlebody" } , "Your email address will not be published")

def searchWorldHinduNews(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"entry-content" })

def searchDailyo(soup , keywords):
	return searchPage2(soup , keywords , "div" , {"class":"mediumcontent" } , 'title="Also read:')

def	searchAvenuemaol(soup , keywords):
	return searchPage(soup , keywords , None , "div.elements-box.mt-20")

def searchHinduExistence(soup , keywords):
	return searchPage(soup , keywords , "div" , {"id":"single" })

def searchHinduHumanRights(soup , keywords):
	return searchPage2(soup , keywords , "div" , {"class":"single-content" } , '<p><a href="http://www.opindia.com/">')

def searchHinduJagruti(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"entry-content" })

def searchMediaCrooks(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"MsoNormal" })
	
def searchDeccanHerald(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"newsText" },1)

def searchDeccanChronicle(soup , keywords):
	return searchPage(soup , keywords , "div" , {"id":"storyBody" })
	
def searchBusinessStandard(soup , keywords):
	result = init_result()
	try:
		content = soup.find_all("div" ,  class_="story-content")
		if content is not None:
			return result
		if len(content) != 1:
			return result
		result["tag_match"] = True
		textContent = content[0].find("span" , class_ = "p-content")
		if genSearchParagraph([textContent] , keywords) is not None:
			result["keyword_match"] = True
	except:
		pass
	return result

def searchHinduBusinessLine(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"article-text" },1)

def  searchTelegraph(soup , keywords):
	result = init_result()
	try:
		p = soup.find("td" ,  class_="articleheader")
		if p is not None:
			result["tag_match"] = True
			table = p.parent.parent
			if genSearchParagraph([table] , keywords) is not None:
				result["keyword_match"] = True
	except:
		pass
	return result		

def searchEconomicTimes(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"section1" })

def searchFirstPost(soup , keywords):	
	return searchPage(soup , keywords , "div" , {"class":"article-full-content" , "itemprop":"articleBody" })

def searchDailyPost(soup , keywords):
	return searchPage2(soup , keywords , "div" , {"class":"post_content" } , 'For more news updates Follow and Like us on')
	
def searchBangaloreMirror(soup , keywords):
	return searchPage(soup , keywords , None , {"id":"storydiv" })
	
def  searchTribuneIndia(soup , keywords):
	return searchPage(soup , keywords , "span" , {"class":"storyText" })
	
def searchAsianAge(soup , keywords):
	return searchPage(soup , keywords , "div" , {"id":"storyBody" })

def searchScroll(soup , keywords):
	return searchPage(soup , keywords , None , "section.article-content.scroll-article-content.latest-article-content")

def searchTelanganaToday(soup , keywords):
	return searchPage(soup , keywords , None , "div.entry-content")

def searchBetterIndia(soup , keywords):
	return searchPage(soup , keywords , None , {"itemprop":"articleBody" } , 1)

def searchFinancialExpress(soup , keywords):
	return searchPage(soup , keywords , "div" , {"itemprop":"articleBody" , "class":"main-story-content" } , 1)

def searchFreePressJournal(soup , keywords):
	return searchPage(soup , keywords , "div" , {"itemprop":"articleBody" })

def searchGreaterKashmirJournal(soup , keywords):
	return searchPage(soup , keywords , "span" , {"class":"storyText" })

def searchMumbaiMirror(soup , keywords):
	return searchPage(soup , keywords , "div" , {"id":"storydiv" } , 1)

def searchNagalandPost(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"NewsDetail" } )

def searchDailyPioneer(soup , keywords):
	return searchPage(soup , keywords , "span" , {"itemprop":"articleBody" } )
	
def searchStateTimes(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"pf-content" } )

def searchStarOfMysore(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"entry-content" } )

def searchNacHindTimes(soup , keywords):
	result = init_result()
	try:
		p = soup.find("article" )
		if p is not None:
			result["tag_match"] = True
			content = p.find("div" , class_="post-inner")
			if genSearchParagraph(content.find_all("p") , keywords) is not None:
				result["keyword_match"] = True
	except:
		pass
	return result		

def searchMorungExpress(soup , keywords):
	return searchPage2(soup , keywords , None , {"id":"main2"  } , 'class="meta_permalink">')
	
def searchNewsTodayNet(soup , keywords):
	return searchPage(soup , keywords , "div" , {"itemprop":"articleBody" } )

def searchTheShillongTimes(soup , keywords)	:
	return searchPage4(soup , keywords , None , "div.single-post-content.entry-content" )

def searchNewsGram(soup , keywords):
	return searchPage(soup , keywords , None , "div.td-post-content" )

def searchPacificMedia(soup , keywords):
	return searchPage(soup , keywords , None , {"class":"entry-content"} )
	
def searchHaindavakeralam(soup , keywords):
	return searchPage(soup , keywords , None , {"id":"news-item"} )
	
def searchSays(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"story-middle"} )
	
def searchChakraNews(soup , keywords):
	return searchPage(soup , keywords , "article" , {"itemtype":"http://schema.org/CreativeWork"} )

def searchMysteryOfIndia(soup , keywords):
	return searchPage(soup , keywords , "div" , {"class":"td-post-content"} )

def	searchDharmaToday(soup , keywords):
	return searchPage(soup , keywords , "div" , {"id":"blog-post-body-content"} )

def searchPostcardNews(soup , keywords):
	return searchPage(soup , keywords , "article" , {} )
	
def genSearchParagraph(elements , keywords):
	for p in elements:
		for searchText in keywords:
			if(p.get_text().find(searchText)) > -1 :
				return searchText
	return None

def filterParagraphs(paragraphs , searchText):
	idx = 0
	for i in paragraphs:
		if(str(i).find(searchText)) > -1:
			break
		idx+=1
	newp =  paragraphs[:idx]
	return newp

def log_error(error_str):
	err_log_f = open("error.log" , "a+")
	err_log_f.write(error_str)
	err_log_f.write("\n")
	err_log_f.close()	
	
#done to truncate the result file before the run.
open("result.txt" , "w").close()
def log_result(result_str):
	f = open("result.txt" , "a+")
	f.write(result_str)
	f.write("\n")
	f.close()
	
def init_result():
	result = {"keyword_match":False , "tag_match":False , "headline" : "" , "author" : ""}
	return result

def get_keywords():
	k = open("news_keyword.txt" , "r")
	keywords = []
	for line in k:
		t = line.strip()
		if len(t) > 0:
			keywords.append(" "+ t +" ")
	k.close()
	return keywords

def init_document():
	pattern = "%B-%d-%Y on %B %d, %Y"
	document = {}
	date_as_string = datetime.datetime.now().strftime(pattern)
	date_as_epoch = int(time.time())
	document["_id"] = date_as_epoch
	document["date_as_string"] = date_as_string
	return document
	
def init_logging():
	logging.basicConfig(level=logging.DEBUG,
                    filename='error.log',
                    filemode='w')
	logging.getLogger().setLevel(logging.ERROR)
# main
def main():
	keywords = get_keywords()
	document = init_document()
	init_logging()
	#initialize database
	try:
		client = MongoClient()
		db = client["news_scraper"]
	except:
		logging.getLogger().exception("Mongd exception")	
	if len(sys.argv) > 1 :
		mode = sys.argv[1].strip()
		if mode == "test":
			logging.getLogger().setLevel(logging.INFO)
			config.mode = "test"
			config.url_visited_check = False
			if len(sys.argv) > 2 and sys.argv[2] is not None and sys.argv[2] == "-f":
				rUrl = sys.argv[3].strip()
				o = urlparse(rUrl)
				list = []
				searchUrl(rUrl, 2, keywords, o.netloc , list , document , db)
				print(document)
				return

	curtime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

	log_result(curtime)
	# initialize the document that needs to be written to the database
	document = init_document()
	f = open("news_websites.txt" , "r")
	for line in f:
		print("Processing " + line + "\n")
		rUrl = line.strip()
		o = urlparse(rUrl)
		list = []
		searchUrl(rUrl, 1, keywords, o.netloc , list , document , db)
	f.close()
	curtime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
	log_result(curtime)
	print(document)
	save_result(document , db)
	client.close()

def save_result(document , db):
	#Write the document to mongo db.
	try:
		collection = db["scraping_result"]
		collection.replace_one({"_id":document["_id"]} , document, upsert=True)
	except:
		logging.getLogger().exception("")

def is_url_visited(url , db):
	res = False
	if config.url_visited_check == False:
		return False
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
