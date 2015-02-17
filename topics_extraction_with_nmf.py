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

This script has been commandeered in order to process resume data.
"""

# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
#         Rahul Verma <rahul.verma@berkeley.edu>
# License: BSD 3 clause

from __future__ import print_function
from time import time
from os import listdir

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import SparsePCA
from scipy import io
from sklearn.datasets import fetch_20newsgroups

n_samples = 2000
n_features = 2000
n_topics = 19
n_top_words = 20


t0 = time()
print("Loading dataset and extracting TF-IDF features...")

vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                             stop_words='english')

paths = ['output/' + i for i in listdir('./output')]
documents = []

for path in paths:
    with open(path) as f:
        try:
            data = f.read().lower()
            string = ''
            for i in data:
                if i in '+abcdefghijklmnopqrstuvwxyz ':
                    string += i
                else:
                    string += ''
            data = string.encode(errors='ignore').strip()
            documents.append(data)
        except Exception as e:
            print(e)
            continue
            

exit
tfidf = vectorizer.fit_transform(documents)
print("done in %0.3fs." % (time() - t0))

# Fit the NMF model
print("Fitting the NMF model with n_samples=%d and n_features=%d..."
      % (n_samples, n_features))

nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

feature_names = vectorizer.get_feature_names()

for topic_idx, topic in enumerate(nmf.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
