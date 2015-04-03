import urllib2
import re
from os import system

def main():
    list_page_url_base = "http://www.indeed.com/resumes/software-engineer/in-California?co=US&start="
    count = 0
    for i in xrange(500, 1000, 50):
        list_page_url = list_page_url_base + str(i)
        list_page = urllib2.urlopen(list_page_url).read()
        for url in re.findall(r'href="(/r/[^"]*)"', list_page):
            try:
                print "Scraping resume:  {}".format(count)
                resume_page = urllib2.urlopen("http://www.indeed.com" + url).read()
                link = re.findall(r'href="([^"]*pdf)"', resume_page)[0]
                system("""wget -q -O 'resumes/{}.pdf' '{}'""".format(count, link))
                count += 1
            except Exception:
                print "Error:   " + link 
                continue

if __name__ == "__main__":
    main()
