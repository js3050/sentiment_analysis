# sentiment_analysis
What does the business need?
 -> The movie producers need to understand if their movie is popular or not.

Data understanding and prep:

    We looked at the combined dataset and figured out that it was well balanced which is good.
     -> TODO: Attach Image

    Further, we can see that there are many words that can through our model of track and these
    need to be cleaned.
    Example : tags like "</br>", spaces, punctuation marks and so on.

    Cleaning of the data has been done in 4 stages:
        1) Handle emojis
            -> These are very important for sentiment analysis and need to be preserved.
        2) Convert all text to lowercase
        3) Remove html tags
        4) Remove remove punctuations


   Tokenizer:
   
       TweetTokenizer chosen because it performs better than the others by taking into account emojis, etc.

   Stemming:
   
        Stemming not done because it may destroy some of our features
        For example : Complicate (negative) nad compliment(positive) are stemmed to => comply
        

   Handling emojis:
   
        Emojis are very important and we replace each emoji with the text it represents
        example:
            :) is replaced with "happy"

   NLTK Stop words used:
   
        NLTK stop words would remove important features
        ex : mustn't, shouldn't, etc

Installation and Usage:

    1) Install mysql
    2) Open mysql shell
    3) Create database with name =  "sentiment_store"
    4) Please enter your username and password on line 8 and 9
    5) Run main.py
        -> This combines the 2 data sources and stores it in a table called data_dump
        -> Then it reads data from data_dump.
        -> Cleans the entire dataset and preps it for running on a ML model
