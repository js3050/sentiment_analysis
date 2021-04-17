from sklearn import metrics
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt


class MachineLearningModel:
    __slots__ = "modelList", "trainingData", 'testingData', 'testLabels', 'train_labels', 'results'

    def __init__(self, X, y_train, Y, y_test):
        self.modelList = [SVC('rbf', 0.02), RandomForestClassifier(n_estimators=50)]
        self.trainingData = X
        self.testingData = Y
        self.testLabels = y_test
        self.train_labels = y_train
        self.results = {}

    def execute_classifiers(self):
        for i in range(len(self.modelList)):
            fit_obj = self.modelList[i].fit(self.trainingData, self.train_labels)
            result = fit_obj.predict(self.testingData)
            self.results[type(self.modelList[i]).__name__] = metrics.accuracy_score(result, self.testLabels)

        print(self.results)

    def visualize_results(self):
        keys = self.results.keys()
        values = self.results.values()
        plt.bar(keys, values)
