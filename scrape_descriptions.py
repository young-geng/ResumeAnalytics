from bs4 import BeautifulSoup
import re
import urllib.request

# returns a list of the id numbers (strings) for every listing matching a certain search criteria, up to num_pages
def get_page_ids(position="software+engineer", location="California", num_pages=1): 		#use "+" for spaces		
	base_url = "http://www.indeed.com/jobs?q=" + position + "&l=" + location + "&start=";		# append 10, 20, 30... for more pages

	all_post_ids = [];

	for i in range(num_pages):
		sock = urllib.request.urlopen(base_url+str((i+1)*10))
		filename = sock.read() 
		sock.close()
		post_ids = re.findall("jobmap\[.\]= {jk:.'................", str(filename))
		for i in range(len(post_ids)):
			post_ids[i] = post_ids[i][17:]
		for i in post_ids:
			all_post_ids.append(i)
	return all_post_ids

# parses the actual listings to get job titles and descriptions
# removes html tags and new lines, appends the title to the description
# returns a list of all of the combined job postings (strings)
def get_listings(post_ids=get_page_ids()):
	jobs = []
	for p_id in post_ids:
		sock = urllib.request.urlopen("http://www.indeed.com/viewjob?jk=" + p_id)
		filename = sock.read()
		sock.close()
		soup = BeautifulSoup(filename)

		title = soup.find("div", {"id": "job_header"})
		title = re.sub("<.[^\<>]*>", "", str(title))	# strip out html tags
		title = re.sub("<\.[^\<>]*>", "", str(title))	# strip out html tags
		title = re.sub("\n", "", str(title))	# strip out newlines

		description = soup.find("span", {"id": "job_summary"})
		description = re.sub("<.[^\<>]*>", "", str(description))	# strip out html tags
		description = re.sub("<\.[^\<>]*>", "", str(description))	# strip out html tags
		description = re.sub("\n", "", str(description))	# strip out html tags

		jobs.append(str(title)+str(description))

	return jobs