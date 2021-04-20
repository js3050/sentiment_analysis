from sklearn import metrics
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from wordcloud import WordCloud, STOPWORDS
from DataInsight import DataInsights
from sklearn.cluster import DBSCAN

import pandas as pd
import gensim
from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class MachineLearningModel:
    __slots__ = "modelList", "trainingData", 'testingData', 'testLabels', 'train_labels', 'results'

    def __init__(self, X_train, y_train, X_test, y_test):
        self.modelList = [RandomForestClassifier(n_estimators=200), MLPClassifier(), KNeighborsClassifier(3),
                          DecisionTreeClassifier()]
        self.trainingData = X_train
        self.testingData = X_test
        self.testLabels = y_test
        self.train_labels = y_train

        self.results = {}

    def execute_classifiers(self):
        for i in range(len(self.modelList)):
            fit_obj = self.modelList[i].fit(self.trainingData, self.train_labels)
            result = fit_obj.predict(self.testingData)
            self.results[type(self.modelList[i]).__name__] = metrics.accuracy_score(result, self.testLabels)
            print('Done with', type(self.modelList[i]).__name__)
        print("Classification Results = ", self.results)

    def DBSCAN(self):
        model = DBSCAN(eps=40, min_samples=50)
        model.fit(self.trainingData)
        res = model.fit_predict(self.testingData)
        print(metrics.accuracy_score(res, self.testLabels))

    def Kmeans(self, original_test_data):
        model = KMeans(n_clusters=7, max_iter=400)
        km = model.fit(self.trainingData)

        res = km.predict(self.testingData)

        print(metrics.accuracy_score(res, self.testLabels))

    def visualize_results(self):
        keys = self.results.keys()
        values = self.results.values()
        plt.bar(keys, values)
        plt.savefig("Classification.png")
        plt.show()
