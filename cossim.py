import numpy as np
import sqlite3

# Both formal parameters should be lists of equal length
# each index should contain the words in that topic
def cossim(database_name, num_listings):
	listings_topics = get_topics()
	curmatrix = ""
	con = sqlite3.connect(database_name)
	con.row_factory = sqlite3.Row

	cur = con.cursor()
	cur = cur.execute("select * from resumes")
	resumes = []
	for row in cur:
		resumes.append(row)

	for i in range(len(resumes)):
		doc = str(resumes[i][1])
		for j in range(len(listings_topics)):
			total = 0
			for k in range(len(listings_topics[j])):
				total += doc.count(listings_topics[j][k])
			curmatrix += str(total) + " "
		curmatrix += "; "
	curmatrix = curmatrix[:-2]
	resume_matrix = np.matrix(curmatrix)

	curmatrix = ""
	for i in range(num_listings):
		f = open("output/job"+str(i+1)+".txt", "r")
		doc = f.read()
		for j in range(len(listings_topics)):
			total = 0
			for k in range(len(listings_topics[j])):
				total += doc.count(listings_topics[j][k])
			curmatrix += str(total) + " "
		curmatrix += "; "
	curmatrix = curmatrix[:-2]

	listing_matrix = np.matrix(curmatrix)

	dotted = np.dot(resume_matrix, listing_matrix.getT()).getA()

	resume_norm = np.sum(np.square(resume_matrix), axis=1)
	listing_norm = np.sum(np.square(listing_matrix), axis=1)

	norm_dotted = np.dot(resume_norm, listing_norm.getT()).getA()

	# np.divide() wasn't cooperating, I guess b/c they're ints
	to_return = [[0 for x in range(num_listings)] for x in range(len(resumes))] 
	for i in range(len(resumes)):
		for j in range(num_listings):
			to_return[i][j] = float(dotted[i][j]) / float(norm_dotted[i][j])
	return to_return, norm_dotted, dotted

# Retrieves topics saved in a txt file called "topics.txt"
def get_topics():
	f = open("topics.txt", "r")
	num_topics = int(f.readline().replace("\n", ""))
	num_words = int(f.readline().replace("\n", ""))
	topics = []
	for i in range(num_topics):
		topics.append([])
		for j in range(num_words):
			topics[i].append(f.readline().replace("\n", ""))

	return topics



