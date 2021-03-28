from DatabaseConnection import DatabaseConnector
from nltk.tokenize import TweetTokenizer
import json


# string = "#throwbackthursday: Coolest fan we’ve ever seen. pic.twitter.com/Ll82Zi7Xug"


# TODO: code for stemming string?

class PreProcess:

    def __init__(self):
        self.conn = self.connect_to_database()
        self.db_cursor = self.conn.mydb.cursor()

    def tokenize_data(self, input_string):
        """
        :param input_string: Any Input text to be tokenized
        :return: List of Tokens
        """
        token_obj = TweetTokenizer()  # init tokenizer object
        return token_obj.tokenize(input_string)

    def read_data(self):
        sql_query = "Select * from data_dump;"
        self.db_cursor.execute(sql_query)
        text_data = self.db_cursor.fetchall()

        token_store = []
        json_tokenized_string = ""
        for i in range(len(text_data)):
            raw_string = text_data[i]
            tokenized_string = self.tokenize_data(raw_string[0])
            json_tokenized_string = json.dumps(tokenized_string)
            token_store.append([json_tokenized_string])

        self.conn.create_pre_process_table()
        self.conn.insert_row_pre_process_table(token_store)
        self.conn.mydb.commit()

    def preprocess_data(self):
        pass

    def connect_to_database(self):
        connector = DatabaseConnector(
            host="localhost",
            user="chaitanya",
            passwd="root",
            database_name="sentiment_store"
        )

        return connector


if __name__ == '__main__':
    pre_processObj = PreProcess()
    pre_processObj.read_data()
    print("Preprocessing done")
