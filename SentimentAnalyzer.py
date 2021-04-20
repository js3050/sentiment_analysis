import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


from MachineLearningModel import MachineLearningModel


class SentimentAnalyzer:
    """
    This class is responsible for performing the analysis operations on the preprocessed data
    """
    __slots__ = "database", "cursor", "dataset", "X_train", "X_test", "y_train", "y_test", "model",'og_test_data'

    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()
        self.og_test_data = None
        self.get_data()
        self.split_data()
        # self.generate_tfidf_mapping()
        self.model = MachineLearningModel(self.X_train, self.y_train, self.X_test, self.y_test)

        #self.model.execute_classifiers()
        #self.model.visualize_results()
        #self.model.Kmeans(self.og_test_data)
        self.model.DBSCAN()


    def get_data(self):
        """
        Fetches preprocessed data from the database
        :return: None
        """
        sql_query = "SELECT * FROM PREPROCESSTABLE;"
        self.cursor.execute(sql_query)
        self.dataset = self.cursor.fetchall()

    def split_data(self):
        """
        Splits the preprocessed data into train and test sets and generate the TF-IDF mapping
        :return: None
        """
        x = []
        y = []
        for each in self.dataset:
            x.append(" ".join(json.loads(each[0])))
            y.append(each[1])

        x = pd.DataFrame(x)
        y = pd.DataFrame(y)
        y = y.replace({
            "positive": 1, "negative": 0
        })
        self.og_test_data = train_test_split(x, y, test_size=0.3)[1]
        x = self.generate_tfidf_mapping(x)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.3)

    def generate_tfidf_mapping(self, x):
        """
        This method generates the Tf-Idf mapping
        :param x: Input matrix
        :return: TF-IDF mapping -> np array
        """
        tfidf_vectorizer = TfidfVectorizer(lowercase=False, analyzer='word')
        return tfidf_vectorizer.fit_transform(x[0])
