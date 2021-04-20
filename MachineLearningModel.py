from sklearn import metrics
from sklearn.metrics import silhouette_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from DataInsight import DataInsights
import matplotlib.pyplot as plt


class MachineLearningModel:
    """
    This class is a generic class that runs builds and runs several machine learning models on the preprocessed data
    """
    __slots__ = "modelList", "trainingData", 'testingData', 'testLabels', 'train_labels', 'results'

    def __init__(self, X_train, y_train, X_test, y_test):
        self.modelList = [RandomForestClassifier(n_estimators=200), MLPClassifier(), KNeighborsClassifier(3),DecisionTreeClassifier()]
        self.trainingData = X_train
        self.testingData = X_test
        self.testLabels = y_test
        self.train_labels = y_train
        self.results = {}

    def execute_classifiers(self):
        """
        This method is responsible for execution of all models specified in the modelList of the class
        :return: None
        """
        for i in range(len(self.modelList)):
            fit_obj = self.modelList[i].fit(self.trainingData, self.train_labels)
            result = fit_obj.predict(self.testingData)
            self.results[type(self.modelList[i]).__name__] = metrics.accuracy_score(result, self.testLabels)
            self.results[type(self.modelList[i]).__name__ + "_f1"] = metrics.f1_score(result, self.testLabels)
            print('Done with', type(self.modelList[i]).__name__)
        print("Classification Results = ",self.results)

    def __get_elbow(self):
        """
        This method returns the silhouette score for the KMeans clustering method
        :return:None
        """
        sil_score = []
        K = range(2, 10)
        for k in K:
            model = KMeans(n_clusters=k, max_iter=200)
            km = model.fit_predict(self.trainingData)
            sil_score.append(silhouette_score(self.trainingData, km))

        print(sil_score)
        plt.figure(figsize=(16, 8))
        plt.plot(K, sil_score, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Silhouette Score')
        plt.title('The Elbow Method showing the optimal k')
        plt.savefig("outs\elbow.png")
        plt.show()

    def Kmeans(self,original_test_data):
        """
        This method runs Kmeans clustering on the given input data
        :param original_test_data: X
        :return:
        """
        self.__get_elbow()
        cluster_count = 3
        model = KMeans(n_clusters=cluster_count)
        km = model.fit(self.trainingData)
        res = km.predict(self.testingData)

        pred_dict = {}
        for i in range(cluster_count):
            pred_dict[i] = []
        pred_one = []
        pred_zero = []
        for i in range(len(res)):
            pred_dict[res[i]].append(original_test_data.iloc[i])

        datas_obj = DataInsights()
        for i in range(len(pred_dict.keys())):
            datas_obj._gen_cloud(pred_dict.get(i), f"outs\{pred_dict.keys()[i]}.png")

        print(metrics.accuracy_score(res, self.testLabels))

    def visualize_results(self):
        """
        This method visualizes results using matplotlib
        :return:
        """
        keys = self.results.keys()
        values = self.results.values()
        plt.bar(keys, values)
        plt.savefig("Classification.png")
        plt.show()

