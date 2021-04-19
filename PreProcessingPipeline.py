import re

from DatabaseConnection import DatabaseConnector
from nltk.tokenize import TweetTokenizer
from nltk.corpus import wordnet
from nltk import pos_tag

from nltk.stem.wordnet import WordNetLemmatizer
import json
import string
from typing import List
import spacy
import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

STOPWORDS = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
             'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
             'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
             'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
             'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',
             'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
             'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
             'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
             'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
             "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
             'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
             "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
             "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
             "wouldn't"}


class PreProcessingPipeline:

    def __init__(self, conn):
        self.conn = conn
        self.db_cursor = self.conn.mydb.cursor()
        self.nlp = spacy.load('en_core_web_sm')

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
        #
        x = re.sub(r"['-?-!]", '', tokenized_string)
        x = re.sub(r"[^a-zA-Z]", ' ', x)
        x = re.sub(r'\s', ' ', x)
        x = re.sub(r' +', ' ', x)
        # x = tokenized_string.translate(str.maketrans('', '', string.punctuation)).strip()
        return x.split()

    def remove_stop_words(self, textList):
        new_list = []

        for i in range(len(textList)):
            if textList[i] not in STOPWORDS:
                new_list.append(textList[i])

        return new_list

    def stemWords(self, textList):
        new_list = []
        tag = pos_tag(textList)
        for i in range(len(textList)):
            lemmatizer = WordNetLemmatizer()
            pos = 'v'
            if tag[i][1][0] == 'J':
                pos = wordnet.ADJ
            elif tag[i][1][0] == 'V':
                pos = wordnet.VERB
            elif tag[i][1][0] == 'N':
                pos = wordnet.NOUN
            elif tag[i][1][0] == 'R':
                pos = wordnet.ADV

            new_word = lemmatizer.lemmatize(textList[i], pos=pos)
            new_list.append(new_word)

        return new_list

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
        x = 0
        for i in range(len(text_data)):
            raw_string = text_data[i]
            tokenized_list = self.tokenize_data(raw_string[0])

            # test_list = ['chai', 'is', ':)', 'WHAT </br> !!! YO....']
            # Perform preprocessing
            update_emo_list = self.handle_emojis(tokenized_list)
            update_lower_case_list = self.to_lowerCase(update_emo_list)
            updated_html_tags = self.remove_html_tags(update_lower_case_list)
            tokenized_list = self.remove_punctuations(updated_html_tags)
            tokenized_list = self.remove_stop_words(tokenized_list)
            tokenized_list = self.stemWords(tokenized_list)
            json_tokenized_string = json.dumps(tokenized_list)
            token_store.append([json_tokenized_string, raw_string[1]])

            if len(token_store) == 10000:
                x += 1
                print("Commit id ", x)
                self.conn.insert_row_pre_process_table(token_store)
                self.conn.mydb.commit()
                token_store = []
        if token_store:
            self.conn.insert_row_pre_process_table(token_store)
            self.conn.mydb.commit()

# if __name__ == '__main__':

# pre_processObj = PreProcessingPipeline()
# data_dump = 'data_dump'
# pre_processObj.read_data(data_dump)
# print("Preprocessing done")
