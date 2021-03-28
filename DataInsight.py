import mysql.connector
from DatabaseConnection import DatabaseConnector
import matplotlib.pyplot as plt


class DataInsights:
    db = None
    def __init__(self):
        self.db = DatabaseConnector("localhost", "root", "", "sentiment_store")

    def generate_counts_plot(self):
        sql_query = "SELECT sentiment, count(sentiment) from sentiment_store.data_dump group by sentiment;"

        cursor = self.db.cursor
        cursor.execute(sql_query)
        labels = []
        values = []
        for each in cursor:
            labels.append(each[0])
            values.append(each[1])
        x_pos = [index for index, _ in enumerate(labels)]

        plt.bar(x_pos, values, color='#20B5C5')
        plt.xlabel("Instances of rows")
        plt.ylabel("Count")
        plt.title("Data breakdown")
        plt.xticks(x_pos, labels)
        plt.savefig("Data_distribution.png")



d = DataInsights()
d.generate_counts_plot()


