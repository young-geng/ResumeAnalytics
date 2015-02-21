from bs4 import BeautifulSoup
import re
import urllib.request

position = "software+engineer"
location = "California"		#use "+" for spaces
base_url = "http://www.indeed.com/jobs?q=" + position + "&l=" + location + "&start=";		# append 10, 20, 30... for more pages

post_links = [];

for i in range(1):
	sock = urllib.request.urlopen(base_url+str(i*10))
	filename = sock.read() 
	sock.close()
	#soup = BeautifulSoup(filename)
	#post_ids = soup.find_all(re.compile(r))
	post_ids = re.findall("jobmap\[.\]= {jk:.'................", str(filename))
	for i in range(len(post_ids)):
		post_ids[i] = post_ids[i][17:]
	print(post_ids)
