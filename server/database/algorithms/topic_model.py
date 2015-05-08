"""
========================================================
Topics extraction with Non-Negative Matrix Factorization
========================================================
"""


from sklearn.decomposition import NMF


"""
Extract topics from sparse_matrix
Return a pair (transformed_data, topics)
"""
def extract_topics(sparse_matrix, feature_names, n_topics=19, n_top_words=20):

    nmf = NMF(n_components=n_topics, random_state=1)
    transformed_data = nmf.fit_transform(sparse_matrix)

    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topics.append([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
    return transformed_data, topics

