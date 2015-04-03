""" 
TFiDF vectorizer
"""


from sklearn.feature_extraction.text import TfidfVectorizer


"""
TFiDF vectorizer
take a list of documents and return pair (sparse_matrix, feature_names)
"""
def tfidf_vectorize(documents, n_features=2000, max_df=0.95, min_df=2):
    vectorizer = TfidfVectorizer(max_df, min_df, max_features=n_features, stop_words='english')    
    tfidf = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names()
    return tfidf, feature_names

