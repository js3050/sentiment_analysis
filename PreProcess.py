from nltk.tokenize import TweetTokenizer

string = "#throwbackthursday: Coolest fan we’ve ever seen. pic.twitter.com/Ll82Zi7Xug"


#TODO: code for stemming string?

def tokenize_data(input_string):
    """
    :param input_string: Any Input text to be tokenized
    :return: List of Tokens
    """
    token_obj = TweetTokenizer()  # init tokenizer object
    return token_obj.tokenize(string)

