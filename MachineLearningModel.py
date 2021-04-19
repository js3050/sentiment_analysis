from sklearn import metrics
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from wordcloud import WordCloud, STOPWORDS

import pandas as pd
# from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt


class MachineLearningModel:
    __slots__ = "modelList", "trainingData", 'testingData', 'testLabels', 'train_labels', 'results'

    def __init__(self, X_train, y_train, X_test, y_test):
        self.modelList = [RandomForestClassifier(n_estimators=200), MLPClassifier(), KNeighborsClassifier(3),DecisionTreeClassifier()]
        self.trainingData = X_train
        self.testingData = X_test
        self.testLabels = y_test
        self.train_labels = y_train
        # self.vectorizedTrainingData = np.array(Word2Vec(self.trainingData).wv.vectors)
        self.results = {}

    def execute_classifiers(self):
        for i in range(len(self.modelList)):
            fit_obj = self.modelList[i].fit(self.trainingData, self.train_labels)
            result = fit_obj.predict(self.testingData)
            self.results[type(self.modelList[i]).__name__] = metrics.accuracy_score(result, self.testLabels)
            print('Done with', type(self.modelList[i]).__name__)
        print("Classification Results = ",self.results)

    def Kmeans(self):
        model = KMeans(n_clusters=2,max_iter=200)
        km = model.fit(self.trainingData)

        res = km.predict(self.testingData)

        print(res)

    def visualize_results(self):
        keys = self.results.keys()
        values = self.results.values()
        plt.bar(keys, values)
        plt.savefig("Classification.png")
        plt.show()

    def centroidsDict(self,centroids, index):
        a = centroids.T[index].sort_values(ascending=False).reset_index().values
        centroid_dict = dict()

        for i in range(0, len(a)):
            centroid_dict.update({a[i, 0]: a[i, 1]})

        return centroid_dict

    def generateWordClouds(self,centroids):
        wordcloud = WordCloud(max_font_size=100, background_color='white')
        for i in range(0, len(centroids)):
            centroid_dict = self.centroidsDict(centroids, i)
            wordcloud.generate_from_frequencies(centroid_dict)

            plt.figure()
            plt.title('Cluster {}'.format(i))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()