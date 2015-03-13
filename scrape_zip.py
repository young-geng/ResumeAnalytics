from bs4 import BeautifulSoup
from os import system
import re
from urllib import urlopen
import sqlite3
import json
from ParallelMap import parmap







def scrape_page(page_num):
    print page_num
    base_url = 'https://www.ziprecruiter.com/resume-database/search?q=%22software+engineer%22&loc=&latitude=&longitude=&city=&state=&postalCode=&country=&radiusSelect=100&resumePostedWithinSelect=365&minimumDegreeSelect=&experienceSelect=&maxExperienceSelect=&page='
    resumes = []
    sock = urlopen(base_url+str((page_num)))
    results = BeautifulSoup(sock.read())
    pops = results.findAll('tr', attrs = {'class': 'popover-holder'})
    for pop in pops:
        url = 'http://www.ziprecruiter.com' + pop.find('a')['href']
        resid = url.split('preview/')[1].split('?')[0]
        url = 'https://www.ziprecruiter.com/contact/zip-resume/{0}?q=%22software%20engineer%22'.format(resid)
        try:
            j = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
        except:
            continue
        resume = BeautifulSoup(j['html'])
        text = resume.get_text()        
        resumes.append((text, pop.find('p', attrs = {'class': 'font11 grayText tRight'}).get_text().split('ed ')[1]))
    return resumes


def main():
    num_pages = 201
    num_pages = 2
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS resumes")
    cursor.execute(''' CREATE TABLE resumes (resume text, date text)''')
    resumes = map(scrape_page, range(num_pages))
    resumes = reduce(lambda x, y: x + y, resumes)
    print(len(resumes))
    for i in range(len(resumes)):
        cursor.execute('INSERT INTO resumes VALUES (?,?)', (resumes[i][0], dates[i][1])) 

    conn.commit()

if __name__ == "__main__":
    main()

