"""
========================================================
Topics extraction with Non-Negative Matrix Factorization
========================================================

This is a proof of concept application of Non Negative Matrix
Factorization of the term frequency matrix of a corpus of documents so
as to extract an additive model of the topic structure of the corpus.
The output is a list of topics, each represented as a list of terms
(weights are not shown).

The default parameters (n_samples / n_features / n_topics) should make
the example runnable in a couple of tens of seconds. You can try to
increase the dimensions of the problem, but be aware than the time complexity
is polynomial.

"""

# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
# License: BSD 3 clause

from __future__ import print_function
from time import time
import sqlite3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import SparsePCA
from scipy import io
from sklearn.datasets import fetch_20newsgroups


n_features = 3000
n_topics = 30
n_top_words = 80

# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.


print("Loading dataset and extracting TF-IDF features...")


vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                             stop_words='english')

documents = []
connection = sqlite3.connect('resumes.db')
cursor = connection.cursor()
for row in cursor.execute('SELECT resume from resumes'):
    documents.append(row[0])


tfidf = vectorizer.fit_transform(documents)

print(len(documents))
# Fit the NMF model
nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)


feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
