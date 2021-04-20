from DatabaseConnection import DatabaseConnector
from DataGobbler import DataGobbler
from PreProcessingPipeline import PreProcessingPipeline
from SentimentAnalyzer import SentimentAnalyzer

__authors__ = [
    {
        "name": "Jagwant Sehgal",
        "email": "js3050@rit.edu"
    },
    {
        "name" :"Chaitanya Mehta",
        "email": "cm9020@rit.edu"
    }
]

if __name__ == '__main__':
    # toggles database generation and dump. Set to false to skip data dump and processing and directly generate analysis
    run_everything = True
    connector = DatabaseConnector(
        host="localhost",
        user="root",
        passwd="",
        database_name="sentiment_store"
    )
    if run_everything:

        connector.init_tables()
        data_gobbler = DataGobbler(connector.mydb, connector.mydb.cursor())
        data_gobbler.start()

        pre_processObj = PreProcessingPipeline(connector)
        data_dump = 'data_dump'
        pre_processObj.read_data(data_dump)
        print("Preprocessing done")

    sentiment_analysis_test = SentimentAnalyzer(connector.mydb)
