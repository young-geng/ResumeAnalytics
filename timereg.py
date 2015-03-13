# Time regression for resume data
from sklearn.linear_model import LogisticRegression
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import re


def main():
    connection = sqlite3.connect('resumes.db')
    cursor = connection.cursor()
    documents = []
    date_tags = []
    for row in cursor.execute('SELECT resume, date FROM resumes'):
        documents.append(re.sub(r'[0-9]', ' ', row[0]))
        if "2014" in row[1]:
            date_tags.append(0)
        else:
            date_tags.append(1)

    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=2000, stop_words='english')
    designMatrix = vectorizer.fit_transform(documents)
    regressor = LogisticRegression(penalty='l1', tol=0.0001, C=1.0)
    regressor.fit(designMatrix, date_tags)
    coefficient = regressor.coef_
    words = vectorizer.get_feature_names()
    word_strength = [(words[i], coefficient[0, i]) for i in xrange(len(words))]
    word_strength.sort(key=lambda x:x[1])
    for i in xrange(len(word_strength) - 1, len(word_strength) - 1 - 50, -1):
        if word_strength[i][1] == 0:
            break;
        print word_strength[i]

    print "\n\n\n\n\n\n"

    for i in xrange(50):
        if word_strength[i][1] == 0:
            break;
        print word_strength[i]


if __name__ == "__main__":
    main()
