"""
=================================
Handy API wrapper for algorithms
This wrapper is meant only for
proof of concept use.
AVOID USE IF POSSIBLE
=================================
"""

from vectorizer import *
from topic_model import *
from cos_sim import *



"""
Take a list of documents and return the extracted topic
"""
def w_extract_topics(documents, n_words=2000, n_topics=20, n_words_per_topic=100):
    design_matrix, words = tfidf_vectorize(documents, n_words)
    topics = extract_topics(design_matrix, feature_names, n_topics, n_words_per_topic)[1]
    return topics


"""
Cosine similarity for 2 lists of documents
"""
def w_cos_sim(documents_list_1, documents_list_2, n_words=2000):
    design_matrix_1 = tfidf_vectorize(documents_list_1, n_words)[0]
    design_matrix_2 = tfidf_vectorize(documents_list_2, n_words)[0]
    return cos_sim(design_matrix_1, design_matrix_2)



"""
Cosine similarity for 2 lists of documents, based on topic modeling
"""
def w_cos_sim_topics(documents_list_1, documents_list_2, n_words=2000, n_topics=40, n_words_per_topic=100):
    design_matrix_1, words_1 = tfidf_vectorize(documents_list_1, n_words)[0]
    design_matrix_2, words_2 = tfidf_vectorize(documents_list_2, n_words)[0]
    transformed_1 = extract_topics(design_matrix_1, words_1, n_topics, n_words_per_topic)[0]
    transformed_2 = extract_topics(design_matrix_2, words_2, n_topics, n_words_per_topic)[0]

    return cos_sim(transformed_1, transformed_2)




