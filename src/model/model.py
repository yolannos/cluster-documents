from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from fcmeans import FCM
import pickle


class ClusterModel():

    def __init__(self, input_file='in_documents.pkl', model='k_means', n_cluster=6):
        '''
        input_file : trained and cleaned data-set as pickle file
        model : clustering method to apply
        n_cluster : number of chosen cluster
        '''

        self.model_chosen = model
        self.n_cluster = n_cluster
        with open(input_file, 'rb') as f:
            self.in_documents = pickle.load(f)

    def vectorize(self):
        '''
        Convert a collection of raw documents to a matrix of TF-IDF features.

        TFIDF, short for term frequency–inverse document frequency, 
        is a numerical statistic that is intended to reflect how important a word is 
        to a document in a collection or corpus.
        '''

        vectorizer = TfidfVectorizer(analyzer='word', stop_words='english', max_features=8000, max_df=1.0)
        self.trans_vectorizer = vectorizer.fit_transform(self.in_documents) # input must be a list of string aka whole text in one str
        self.vectorizer = vectorizer

    def decompose(self):
        '''
        Dimensionality reduction using truncated SVD
        '''

        decomposition = TruncatedSVD(100)
        self.trans_decomposition = decomposition.fit_transform(self.trans_vectorizer)
        self.decomposition = decomposition

    def k_means(self):
        '''
        K-Means clustering.
        https://scikit-learn.org/stable/modules/clustering.html#k-means
        '''
        
        model_k = KMeans(n_clusters=self.n_cluster, init='k-means++', max_iter=100, n_init=1)
        return model_k.fit(self.trans_decomposition)

    def c_means(self):
        '''
        Fuzzy C-means clustering algorithm
        https://www.sciencedirect.com/science/article/pii/0098300484900207?via%3Dihub
        '''

        model_c = FCM(n_clusters=6)
        return model_c.fit(self.trans_decomposition)

    def cluster(self):
        '''
        Based on the model chosen in the instanciation of the class, call the appropriate method.
        Dump all the necessary tools to make prediction
        '''

        self.vectorize()
        self.decompose()
        model = getattr(self, self.model_chosen)()

        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)

        with open('decomposition.pkl', 'wb') as f:
            pickle.dump(self.decomposition, f)