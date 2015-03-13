from bs4 import BeautifulSoup
from os import system
import re
import urllib.request
import sqlite3
import json

conn = sqlite3.connect('resumes.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS resumes")
cursor.execute(''' CREATE TABLE resumes (id real, resume text, date text)''')


base_url = 'https://www.ziprecruiter.com/resume-database/search?q=%22software+engineer%22&loc=&latitude=&longitude=&city=&state=&postalCode=&country=&radiusSelect=100&resumePostedWithinSelect=365&minimumDegreeSelect=&experienceSelect=&maxExperienceSelect=&page='

num_pages = 201

resumes, dates = [], []

for i in range(num_pages):
    print(i)
    sock = urllib.request.urlopen(base_url+str((i)))
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
        resumes.append(text)
        dates.append(pop.find('p', attrs = {'class': 'font11 grayText tRight'}).get_text().split('ed ')[1])

print(len(resumes))
print(len(dates))
for i in range(len(resumes)):
    cursor.execute('INSERT INTO resumes VALUES (?,?, ?)', (i, resumes[i], dates[i])) 

conn.commit()


