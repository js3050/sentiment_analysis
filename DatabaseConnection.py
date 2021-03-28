import mysql.connector


class DatabaseConnector:
    mydb, database_name, cursor = None, None, None
    host, user, passwd = None, None, None

    def __init__(self, host, user, passwd, database_name):
        print("Initializing database connection")
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database_name = database_name
        self.connect()
        print(self.mydb, " \n initializing tables ... ")
        #self.init_tables()
        print("Complete")



    def connect(self):
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.passwd,
            database=self.database_name
        )
        self.cursor = self.mydb.cursor()


    def init_tables(self):

        self.cursor.execute("DROP TABLE IF EXISTS data_dump")
        self.cursor.execute("CREATE TABLE data_dump (review TEXT, sentiment VARCHAR(255))")

