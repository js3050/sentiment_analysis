import pandas as pd
import json
from sklearn.model_selection import train_test_split
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import string

from MachineLearningModel import MachineLearningModel


class SentimentAnalyzer:
    __slots__ = "database","cursor", "dataset", "X_train", "X_test", "y_train", "y_test", "model"

    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()
        self.get_data()
        self.split_data()
        # self.generate_tfidf_mapping()
        self.model = MachineLearningModel(self.X_train, self.y_train, self.X_test, self.y_test)
        self.model.execute_classifiers()

    def get_data(self):
        sql_query = "SELECT * from sentiment_store.preprocesstable;"
        self.cursor.execute(sql_query)
        self.dataset = self.cursor.fetchall()

    def split_data(self):
        """
        Splits the preprocessed data into train and test sets
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
        x = self.generate_tfidf_mapping(x)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2)

    def generate_tfidf_mapping(self, x):
        tfidf_vectorizer = TfidfVectorizer()
        return tfidf_vectorizer.fit_transform(x[0])
