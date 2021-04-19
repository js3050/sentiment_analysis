from DatabaseConnection import DatabaseConnector
from DataGobbler import DataGobbler
from PreProcessingPipeline import PreProcessingPipeline
from SentimentAnalyzer import SentimentAnalyzer

if __name__ == '__main__':
    run_everything = False
    connector = DatabaseConnector(
        host="localhost",
        user="root",
        passwd="root",
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
