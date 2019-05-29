# -*- coding: utf-8 -*-
import os.path

import sklearn.datasets
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

#Defining the model and training it 
class NewsClassify(object):

    categories = None
    root_path = os.path.dirname(os.path.realpath(__file__))
    vocab_path = os.path.join(root_path, "models/vocab.pickle")
    model_path = os.path.join(root_path, "models/model.pickle")

    def __init__(self, train=False, categories=None):
        if(train):
            print("Starting Train")
            model = self.model(self.categories)
            pickle.dump(model, open(self.model_path, 'wb'))
            print("Training Finished")

        if(categories):
            self.categories = categories

        print("Loading pre-trained model")
        vocabulary_to_load = pickle.load(open(self.vocab_path, 'rb'), encoding='latin1')
        self.count_vect = CountVectorizer(vocabulary=vocabulary_to_load)
        self.load_model = pickle.load(open(self.model_path, 'rb'))

        self.count_vect._validate_vocabulary()
        self.tfidf_transformer = self.tf_idf(self.categories)[0]

    def fetch_train_dataset(self, categories):
        data_path = os.path.join(self.root_path, "news")
        data_stream = sklearn.datasets.load_files(data_path, description=None, categories=categories,load_content=True, shuffle=True,encoding='utf-8',decode_error='strict', random_state=42)
        return data_stream
        
    def bag_of_words(self, categories):
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(self.fetch_train_dataset(categories).data)
        pickle.dump(count_vect.vocabulary_, open(self.vocab_path, 'wb'))
        return X_train_counts
        
    def tf_idf(self, categories):
        tf_transformer = TfidfTransformer(use_idf=False)
        return (tf_transformer,tf_transformer.fit_transform(self.bag_of_words(categories)))

    def model(self, categories):
        clf = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, random_state=42, max_iter=5, tol=None).fit(self.tf_idf(categories)[1], self.fetch_train_dataset(categories).target)
        return clf

    def classify(self, text):
        X_new_counts = self.count_vect.transform([text])
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        predicted = self.load_model.predict(X_new_tfidf)
        return self.fetch_train_dataset(self.categories).target_names[predicted[0]]