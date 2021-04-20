import sys
import os
import pandas as pd

class DataGobbler:
    """
    This class is responsible for reading the input datasets and dumping the same into the MySQL database
    """
    db_cursor = None
    batch_size = 100

    def __init__(self, db, cursor, batch_size=100):
        self.db_cursor = cursor
        self.db = db
        self.batch_size = batch_size
        self.batch_size = 100

    def start(self):
        """
        Starting point
        :return: None
        """
        # imdb
        self.read_data_from_file_imdb()
        # rotten tomatoes
        self.read_data_from_file_rt()

        self.commit_to_db()

    def read_data_from_file_imdb(self):
        """
        This method reads data from the various files in the imdb dataset
        :return: None
        """
        positive_path = "aclImdb/train/pos/"
        negative_path = "aclImdb/train/neg/"
        positive_files = os.listdir(positive_path)
        negative_files = os.listdir(negative_path)
        self._write_batch(positive_files, positive_path, "positive")
        self._write_batch(negative_files, negative_path, "negative")

    def read_data_from_file_rt(self):
        """
        This method reads the rotten tomatoes review csv and converts it to rows on the MySQL Dump
        :return:
        """
        data = pd.read_csv("rotten_tomatoes_reviews.csv")
        #selecting only the first 100,000 rows
        data = data.iloc[:100000, :]
        # change to positive and negative based on fresh score
        data.loc[data['Freshness'] == 0, 'Freshness'] = "negative"
        data.loc[data['Freshness'] == 1, 'Freshness'] = "positive"

        data_list = []
        for index in range(len(data)):
            data_list.append(
                (data.iloc[index, :]['Review'],data.iloc[index, :]['Freshness'])
            )

        print("writing rotten tomatoes data", len(data_list))
        self.write_data(data_list)

    def _write_batch(self, file_listing, path, label):
        """
        This method is responsible for writing data in batches to the mysql database for each file in IMDB dataset
        :param file_listing: list of filenames to read
        :param path: path of files
        :param label: positive / negative
        :return:
        """
        data = []
        start_index = 0
        batch_number = 1
        batch = file_listing[start_index: start_index + self.batch_size]
        while batch:
            for index, each in enumerate(batch):
                f = open(path + file_listing[index])
                data.append((f.read().strip(), label))
            start_index += self.batch_size
            batch = file_listing[start_index: start_index + self.batch_size]
            batch_number += 1

            print(start_index, start_index + self.batch_size)

            self.write_data(data)
            data = []
            print("Batch written", batch_number)

    def write_data(self, data_list):
        """
        This is a helper method used to execute multiple insert queries into the mysql database
        :param data_list: List of elements to dump
        :return: None
        """
        sql_query = "INSERT INTO data_dump (review, sentiment) VALUES(%s, %s);"
        self.db_cursor.executemany(sql_query, data_list)


    def commit_to_db(self):
        """
        Helper method to commit write to db
        :return: None
        """
        self.db.commit()




