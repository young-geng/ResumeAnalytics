from bs4 import BeautifulSoup
# if anyone tells you to try windmill
# don't do it!
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import re
from copy import copy

def get_ids(description="", num_pages=1):
	all_post_ids = []
	driver = webdriver.Firefox()

	for i in range(num_pages):
		cur_url = "https://www.google.com/about/careers/search#t=sq&q=jd=" + description + "&li=10&st=" + str(0*10) + "&jc=SOFTWARE_ENGINEERING&jc=HARDWARE_ENGINEERING&jc=NETWORK_ENGINEERING&jc=USER_EXPERIENCE&jc=TECHNICAL_INFRASTRUCTURE_ENGINEERING&"
		driver.get(cur_url)
		html = driver.page_source

		soup = BeautifulSoup(html, "html5lib")
		id_div = soup.find("div", { "class" : "srs" })
		post_ids = re.findall("id=\".[0-9].[0-9].[0-9].[0-9].[0-9]*", str(id_div))
		for i in range(len(post_ids)):
			post_ids[i] = post_ids[i][4:-1]
		for i in post_ids:
			all_post_ids.append(i)

	return all_post_ids

def get_listings(post_ids):
	reload(sys)  
	sys.setdefaultencoding('utf8')
	jobs = []
	driver = webdriver.Firefox()

	for p_id in post_ids:
		driver.get("https://www.google.com/about/careers/search#!t=jo&jid=" + str(p_id))
		page = driver.page_source
		soup = BeautifulSoup(page, "html5lib")

		title = soup.find("a", {"class": "heading detail-title"})
		title = title.get_text()
		title = re.sub("\n", "", title.encode("utf8"))

		description = soup.find("div", {"itemprop": "description"})
		description = description.get_text()
		description = re.sub("\n", "", description.encode("utf8"))

		jobs.append(title.encode("utf8") + description.encode("utf8"))

	return jobs

# you must have a folder in the same directory 
# called "google_output" for the jobs to be saved to
def write_listings(jobs):
	counter = 1
	for job in jobs:
		f = open("google_output/job"+str(counter)+".txt", "w")
		f.write(job)
		counter += 1

