from DatabaseConnection import DatabaseConnector
from DataGobbler import DataGobbler
from PreProcessingPipeline import PreProcessingPipeline


if __name__ == '__main__':
    connector = DatabaseConnector(
        host="localhost",
        user="root",
        passwd="",
        database_name="sentiment_store"
    )
    connector.init_tables()
    data_gobbler = DataGobbler(connector.mydb, connector.mydb.cursor())
    data_gobbler.start()

    pre_processObj = PreProcessingPipeline(connector)
    data_dump = 'data_dump'
    pre_processObj.read_data(data_dump)
    print("Preprocessing done")
