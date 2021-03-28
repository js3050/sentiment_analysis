
from sklearn import metrics
class MachineLearningModel:
    __slots__ = "ModeList", "trainingData", 'testingData', 'testLabels', 'train_labels', 'results'

    def __init__(self, Model_list, X, train_labels, test_data, test_label):
        self.ModeList = Model_list
        self.trainingData = X
        self.testingData = test_data
        self.testLabels = test_label
        self.train_labels = train_labels
        self.results = {}

    def execute_classifiers(self):
        for i in range(len(self.ModeList)):
            fit_obj = self.ModeList[i].fit(self.trainingData, self.train_labels)
            result = fit_obj.predict(self.testingData)
            self.results[type(self.ModeList[i]).__name__] = metrics.accuracy_score(result,self.testLabels)
