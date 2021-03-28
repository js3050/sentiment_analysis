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
        print(self.mydb, " \n initializing tables ... ")

        self.cursor.execute("DROP TABLE IF EXISTS data_dump")
        self.cursor.execute("CREATE TABLE data_dump (review TEXT, sentiment VARCHAR(255))")

    def create_pre_process_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS preprocesstable;")
        self.cursor.execute("CREATE TABLE preprocesstable (review JSON, sentiment VARCHAR(255));")

    def insert_row_pre_process_table(self,json_text):
        sql_query = '''INSERT INTO preprocesstable (review,sentiment) VALUES(%s, %s);'''
        self.cursor.executemany(sql_query, json_text)


