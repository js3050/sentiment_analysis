from DatabaseConnection import DatabaseConnector
from DataGobbler import DataGobbler

if __name__ == "__main__":

    connector = DatabaseConnector(
        host="localhost",
        user="root",
        passwd="",
        database_name="sentiment_store"
    )
    data_gobbler = DataGobbler(connector.mydb,connector.mydb.cursor())
    data_gobbler.start()



