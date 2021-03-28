from DatabaseConnection import DatabaseConnector
from nltk.tokenize import TweetTokenizer

string = "#throwbackthursday: Coolest fan we’ve ever seen. pic.twitter.com/Ll82Zi7Xug"


#TODO: code for stemming string?

class PreProcess:

    def __init__(self):



    def tokenize_data(input_string):
        """
        :param input_string: Any Input text to be tokenized
        :return: List of Tokens
        """
        token_obj = TweetTokenizer()  # init tokenizer object
        return token_obj.tokenize(string)


    def preprocess_data():
        pass

    def connect_to_database(self):

        connector = DatabaseConnector(
            host="localhost",
            user="chaitanya",
            passwd="root",
            database_name="sentiment_store"
        )
        return connector