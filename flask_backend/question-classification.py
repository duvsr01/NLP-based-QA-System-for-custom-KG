import pickle

# Training data

# X is the sample sentences
X = [
    'How many courses are taught by Dan Harkey?',
    'What is number of faculty in SJSU?',
    'How many machine learning courses are on Coursera?',
    'How many students are in the world?',
    'What is the email of Ram Shyam?',
    'What is the email address of Albert Einstein?',
    'What is the deadline to pay Fall 2021 Tuition Fee?',
    'What are office hours of Vinodh Gopinath?',
    'How many courses are offered by University of Hogwarts?',
    'How to pay tuition fees?',
    'Phone number of Mr Sam Igloo?',
    'How can I get a bus pass?'
]


# y is the intent class corresponding to sentences in X
y = [
    'aggregation_question',
    'aggregation_question',
    'aggregation_question',
    'aggregation_question',
    'factoid_question',
    'factoid_question',
    'factoid_question',
    'factoid_question',
    'aggregation_question',
    'factoid_question',
    'factoid_question',
    'factoid_question'
]

# Define the classifier

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

clf = Pipeline(
    [
        ('tfidf', TfidfVectorizer()),
        ('sgd', SGDClassifier())
    ]
)

## Train the classifier

#clf.fit(X, y)

# Test your classifier

## New sentences (that weren't in X and your model never seen before)

new_sentences = [
    'What is number of students that study in CMPE department?',
    'How can I reach CMPE department?',
    'How to apply for graduation?',
    'How many faulty in CS department?',
    'Number of students CS department?',
    'What is the address of CS department?'
]

#predicted_intents = clf.predict(new_sentences)
filename = 'finalized_model.sav'
#pickle.dump(clf, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
predicted_intents = loaded_model.predict(new_sentences)

print(predicted_intents)