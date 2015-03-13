from bs4 import BeautifulSoup
# required to execute scripts in the page before getting the html
# alternatively, Selinium could probably be used
from windmill.authoring import setup_module, WindmillTestClient
from windmill.conf import global_settings
import sys
import re

global_settings.START_FIREFOX = True # This makes it use Firefox
setup_module(sys.modules[__name__])

def get_ids(description="", num_pages=1):
	all_post_ids = []
	#for i in range(num_pages):
	cur_url = "https://www.google.com/about/careers/search#t=sq&q=jd=" + description + "&li=10&st=" + str(0*10) + "&jc=SOFTWARE_ENGINEERING&jc=HARDWARE_ENGINEERING&jc=NETWORK_ENGINEERING&jc=USER_EXPERIENCE&jc=TECHNICAL_INFRASTRUCTURE_ENGINEERING&"
	client = WindmillTestClient(__name__)
	client.open(url=cur_url)

	# untested
	# client.waits.forElement(xpath=u"//div[@class='srs']", timeout=u'3000')
	client.waits.sleep(milliseconds=2000)

	html = client.commands.getPageText()
	soup = BeautifulSoup(html)
	id_div = soup.find("div", { "class" : "srs" })
	post_ids = re.findall("div id=\".[0-9].[0-9].[0-9].[0-9].[0-9]*", str(id_div))
	for i in range(len(post_ids)):
		post_ids[i] = post_ids[i][8:]
	for i in post_ids:
		all_post_ids.append(i)

	return all_post_ids

def get_listings(post_ids):
	jobs = []
	client = WindmillTestClient(__name__)

	for p_id in post_ids:
		client.open(url="https://www.google.com/about/careers/search#!t=jo&jid=" + str(p_id))
		page = client.commands.getPageText()
		soup = BeautifulSoup(page, "html5")

		title = soup.find("a", {"class": "heading detail-title"})
		title = title.get_text()
		title = re.sub("\n", "", str(title))

		description = soup.find("div", {"itemprop": "description"})
		description = description.get_text()
		description = re.sub("\n", "", str(description))

		jobs.append(str(title)+str(description))

	return jobs

# you must have a folder in the same directory 
# called "google_output" for the jobs to be saved to
def write_listings(jobs):
	counter = 1
	for job in jobs:
		f = open("google_output/job"+str(counter)+".txt", "w")
		f.write(job)
		counter += 1

