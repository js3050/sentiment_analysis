import re

from DatabaseConnection import DatabaseConnector
from nltk.tokenize import TweetTokenizer
import json

from typing import List


class PreProcessingPipeline:

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

    def read_data(self, table_name: str):
        sql_query = f"Select * from {table_name};"
        self.db_cursor.execute(sql_query)
        self.preprocess_data()

    def remove_html_tags(self, text_list: List[str]):
        text_string = ' '.join([str(text_list[i]) for i in range(len(text_list))])

        store = re.sub(r'<.*?>', ' ', text_string).split()

        return store

    def remove_punctuations(self, text: List[str]):

        tokenized_string = ' '.join([str(text[i]) for i in range(len(text))])

        x = re.sub(r"[^a-zA-Z]", ' ', tokenized_string)
        x = re.sub(r'\s', ' ', x)
        x = re.sub(r' +', ' ', x)
        return x.split()

    def handle_emojis(self, text_list: List[str]):
        """
        This finds all emojis in a string and replaces with corresponding word
        :param text_list: List of tokens
        :param text: String of tokens
        :return: list of tokens
        """
        emo_dict = {':)': 'happy', ':(': 'sad', ":/": 'annoyed'}
        for i in range(len(text_list)):
            if text_list[i] in emo_dict:
                text_list[i] = emo_dict.get(text_list[i])
        return text_list

    def to_lowerCase(self, text: List[str]):
        return [text[i].lower() for i in range(len(text))]

    def preprocess_data(self):
        print("Fetching data")
        text_data = self.db_cursor.fetchall()
        print("done")
        token_store = []

        print("Preprocessing..")
        self.conn.create_pre_process_table()

        for i in range(len(text_data)):
            raw_string = text_data[i]
            tokenized_list = self.tokenize_data(raw_string[0])

            # test_list = ['chai', 'is', ':)', 'WHAT </br> !!! YO....']
            # Perform preprocessing
            update_emo_list = self.handle_emojis(tokenized_list)
            update_lower_case_list = self.to_lowerCase(update_emo_list)
            updated_html_tags = self.remove_html_tags(update_lower_case_list)
            tokenized_list = self.remove_punctuations(updated_html_tags)

            json_tokenized_string = json.dumps(tokenized_list)
            token_store.append([json_tokenized_string, raw_string[1]])

            if len(token_store) == 10000:
                self.conn.insert_row_pre_process_table(token_store)
                self.conn.mydb.commit()
                token_store = []
        if token_store:
            self.conn.insert_row_pre_process_table(token_store)
            self.conn.mydb.commit()

    def connect_to_database(self):
        connector = DatabaseConnector(
            host="localhost",
            user="chaitanya",
            passwd="root",
            database_name="sentiment_store"
        )

        return connector


if __name__ == '__main__':
    pre_processObj = PreProcessingPipeline()
    data_dump = 'data_dump'
    pre_processObj.read_data(data_dump)
    print("Preprocessing done")
