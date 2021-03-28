import sys
import os
import pandas as pd

class DataGobbler:
    db_cursor = None
    batch_size = 100

    def __init__(self, db, cursor, batch_size=100):
        self.db_cursor = cursor
        self.db = db
        self.batch_size = batch_size
        self.batch_size = 100

    def start(self):
        # imdb
        self.read_data_from_file_imdb()
        # rotten tomatoes
        self.read_data_from_file_rt()

    def read_data_from_file_imdb(self):
        positive_path = "aclImdb/train/pos/"
        negative_path = "aclImdb/train/neg/"
        positive_files = os.listdir(positive_path)
        negative_files = os.listdir(negative_path)
        self._write_batch(positive_files, positive_path, "positive")
        self._write_batch(negative_files, negative_path, "negative")

    def read_data_from_file_rt(self):
        data = pd.read_csv("datasetSentences.txt", sep="\t")
        data = list(data['sentence'])
        dataset = []
        for each in data:
            dataset.append((each, ""))
        print("writing rotten tomatoes data")
        self.write_data(dataset)

    def _write_batch(self, file_listing, path, label):
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
        sql_query = "INSERT INTO data_dump (review, sentiment) VALUES(%s, %s);"

        self.db_cursor.executemany(sql_query, data_list)
        self.db.commit()
