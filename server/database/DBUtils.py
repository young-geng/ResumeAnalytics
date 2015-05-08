from time import time
from os import listdir

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import SparsePCA
from scipy import io
from sklearn.datasets import fetch_20newsgroups
import sqlite3
import re
from sys import stdout

from algorithms import *


""" Store the content of files into resumes database """
def store_resumes(files):
    conn = sqlite3.connect('analysis.db')
    cur = conn.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS resumes (resume text)")
    for f in files:
        conn.execute("INSERT INTO resumes VALUES (?)", f)


""" Store the content of files into jobs database """
def store_jobs(files):
    conn = sqlite3.connect('analysis.db')
    cur = conn.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS jobs (job text)")
    for f in files:
        conn.execute("INSERT INTO jobs VALUES (?)", f)





""" Return a list of all resumes """
def list_resumes():
    connection = sqlite3.connect('analysis.db')
    cursor = connection.cursor()
    documents = []
    for row in cursor.execute('SELECT resume FROM resumes'):
        documents.append(row[0])
    return documents

""" Return a list of all jobs """
def list_jobs():
    connection = sqlite3.connect('analysis.db')
    cursor = connection.cursor()
    documents = []
    for row in cursor.execute('SELECT job FROM jobs'):
        documents.append(row[0])
    return documents


""" Return a list of list, each inside list contains words for the topic """
def get_topics():
    connection = sqlite3.connect('analysis.db')
    cursor = connection.cursor()
    documents = []
    for row in cursor.execute('SELECT resume FROM resumes'):
        documents.append(row[0])
    return w_extract_topics(documents)
    



""" Return a list of resumes as text file sorted by matchness with descending order """
def find_matching_resume(jobid):
    connection = sqlite3.connect('analysis.db')
    cursor = connection.cursor()
    documents = []
    for row in cursor.execute('SELECT resume FROM resumes'):
        documents.append(row[0])

    for row in cursor.execute('SELECT job FROM jobs WHERE ROWID = {}'.format(jobid)):
        job_text = row[0]

    result = w_cos_sim([job_text], documents)

    result = numpy.ndarray.flatten(result)
    return map(lambda x: x[1], sorted(zip(result, documents), key=lambda x:x[0]))

