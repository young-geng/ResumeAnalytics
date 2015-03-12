from bs4 import BeautifulSoup
import re
import urllib.request

# returns a list of the id numbers (strings) for every listing matching a certain search criteria, up to num_pages
def get_page_ids(position="software+engineer", location="California", num_pages=1): 		#use "+" for spaces		
	base_url = "http://www.indeed.com/jobs?q=" + position + "&l=" + location + "&start=";		# append 10, 20, 30... for more pages

	all_post_ids = [];

	for i in range(num_pages):
		sock = urllib.request.urlopen(base_url+str((i)*10))
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

# Known bug: Some downloaded pages have apparent html tag errors.  
# The commands that strip out html tags may strip some of the text as well if such errors exist.
def get_listings(post_ids=get_page_ids()):
	jobs = []
	for p_id in post_ids:
		sock = urllib.request.urlopen("http://www.indeed.com/viewjob?jk=" + p_id)
		filename = sock.read()
		sock.close()
		soup = BeautifulSoup(filename, "html5")

		title = soup.find("div", {"id": "job_header"})
		title = title.get_text()
		title = re.sub("\n", "", str(title))

		description = soup.find("span", {"id": "job_summary"})
		description = description.get_text()
		description = re.sub("\n", "", str(description))

		jobs.append(str(title)+str(description))

	return jobs

# Writes the contents of each element in jobs into its own text file
# Assumes you have a folder in the same directory called "output" to hold the text files
# Job files will be named "jobx.txt" where x is a number from 1 to len(jobs)
def write_listings(jobs):
	counter = 1
	for job in jobs:
		f = open("output/job"+str(counter)+".txt", "w")
		f.write(job)
		counter += 1





