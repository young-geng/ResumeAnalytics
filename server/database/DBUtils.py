import sqlite3



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
    pass

""" Return a list of all jobs """
def list_jobs():
    pass



""" Return a list of list, each inside list contains words for the topic """
def get_topics():
    pass



""" Return a list of resumes as text file sorted by matchness with descending order """
def find_matching_resume(jobid):
    pass
