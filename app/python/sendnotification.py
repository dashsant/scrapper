import os
import datetime
#echo "MESSAGE BODY" | mailx -s "SUBJECT" -a "FILEPATH" -a "ANOTHERFILE" USER@DOM.TLD
d = datetime.date.today()
subject = "Result for  " + d.strftime("%A %d. %B %Y")

command = 'echo "Please find the attached result - Niyhyanandam" | mailx -s ' + '"' + subject + '"' + ' -a "/root/scrapper/app/python/result.txt" ' + ' -a "/root/scrapper/app/python/news_keyword.txt" ' + ' -a "/root/scrapper/app/python/news_websites.txt" sri.ramanatha@nithyananda.org '

os.system(command)



