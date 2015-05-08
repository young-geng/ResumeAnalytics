import numpy as np
import sqlite3
from sklearn.preprocessing import normalize

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
	#return listing_matrix.getA()

	#dotted = np.dot(resume_matrix, listing_matrix.T()).getA()

	#resume_norm = np.linalg.norm(resume_matrix, axis=1)
	#listing_norm = np.matrix(np.linalg.norm(listing_matrix, axis=1)).getT()

	#row_sums = resume_matrix.sum(axis=1)
	#resume_norm = resume_matrix / row_sums[:, np.newaxis]

	#row_sums = listing_matrix.sum(axis=1)
	#listing_norm = listing_matrix / row_sums[:, np.newaxis]

	resume_matrix = resume_matrix.astype(float)
	listing_matrix = listing_matrix.astype(float)
	A_norm = np.sum(np.square(resume_matrix), axis=1)
	B_norm = np.sum(np.square(listing_matrix), axis=1)
	product = resume_matrix.dot(listing_matrix.T)
	#check_for_zeroes(product)
	#return (A_norm.dot(B_norm.T)).getA();
	return product / (A_norm.dot(B_norm.T))



	#print listing_norm
	#resume_norm = np.sum(np.square(resume_matrix), axis=1)
	#listing_norm = np.sum(np.square(listing_matrix), axis=1)

	#norm_dotted = np.dot(resume_norm, listing_norm.T)

	#return norm_dotted

	# np.divide() wasn't cooperating, I guess b/c they're ints
	#to_return = [[0 for x in range(num_listings)] for x in range(len(resumes))] 
	#for i in range(len(resumes)):
	#	for j in range(num_listings):
	#		to_return[i][j] = float(dotted[i][j]) / float(norm_dotted[i][j])
	#return to_return

# checks if any vector is all zeroes
def check_for_zeroes(matrix):
	for i in range(len(matrix)):
		x = True
		for j in range(len(matrix[i])):
			if matrix[i][j] != 0:
				x = False
		if x:
			print "BAD:"
			print i

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

# Prints the best candidate for each job
def find_max_job(results):
	#results = results.getA()
	#for i in range(len(results[0])):
	#	maximum = -1
	#	maxrow = -1
	#	for j in range(len(results)):
	#		if results[j][i] > maximum:
	#			maximum = results[j][i]
	#			maxrow = j
	#	print "The best candidate for job #" + str(i+1) + " is: Candidate #" + str(maxrow+1) + " with a score of " + str(results[maxrow][i])
	max_indices = np.argmax(results.getT(), axis=1)
	for i in range(len(max_indices)):
		print "The best job for candidate number #" + str(i+1) + " is job #" + str(max_indices.getA()[i][0]+1)

		
# Prints the best job for each candidate
def find_max_candidate(results):
	#results = results.getA()
	#for i in range(len(results)):
	#	maximum = -1
	#	maxcol = -1
	#	for j in range(len(results[i])):
	#		if results[i][j] > maximum:
	#			maximum = results[i][j]
	#			maxcol = j
	max_indices = np.argmax(results, axis=1)
	for i in range(len(max_indices)):
		print "The best job for candidate number #" + str(i+1) + " is job #" + str(max_indices.getA()[i][0]+1)



