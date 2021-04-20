from DatabaseConnection import DatabaseConnector
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud, STOPWORDS


class DataInsights:
    db = None
    cursor = None

    def __init__(self):
        self.db = DatabaseConnector("localhost", "root", "", "sentiment_store")
        self.cursor = self.db.cursor

    def generate_counts_plot(self):
        sql_query = "SELECT sentiment, count(sentiment) from sentiment_store.data_dump group by sentiment;"

        self.cursor.execute(sql_query)
        labels = []
        values = []
        for each in self.cursor:
            labels.append(each[0])
            values.append(each[1])
        x_pos = [index for index, _ in enumerate(labels)]

        plt.bar(x_pos, values, color='#20B5C5')
        plt.xlabel("Instances of rows")
        plt.ylabel("Count")
        plt.title("Data breakdown")
        plt.xticks(x_pos, labels)
        plt.savefig("Data_distribution.png")

    def generate_word_cloud(self):
        print("Generating word cloud")
        sql_query_pos = "SELECT review from sentiment_store.preprocesstable where sentiment='positive'"
        sql_query_neg = "SELECT review from sentiment_store.preprocesstable where sentiment='negative'"
        self.cursor.execute(sql_query_pos)
        data = self.cursor.fetchall()
        data = [json.loads(n[0]) for n in data]
        self._gen_cloud(data)
        self.cursor.execute(sql_query_neg)
        data = self.cursor.fetchall()
        data = [json.loads(n[0]) for n in data]
        self._gen_cloud(data)



    def _gen_cloud(self, data, file_name="wordcloud.png"):
        wordstring = ""
        for each_string in data:
            for each_word in each_string:
                wordstring += each_word + " "

        wcloud = WordCloud(width=800, height=800, background_color="black", stopwords=STOPWORDS,
                           min_font_size=9).generate(wordstring)
        plt.figure(figsize=(10, 10), facecolor=None)
        plt.imshow(wcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.show()
        plt.savefig(file_name)


if __name__ == '__main__':
    d = DataInsights()
    # d.generate_counts_plot()
    d.generate_word_cloud()
