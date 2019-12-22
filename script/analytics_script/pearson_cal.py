from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import udf


class PearsonCorrelationCalculator:
    def __init__(self):
        """
        Initialises a Spark session and object attributes for later processing
        """
        self.spark_session = SparkSession \
            .builder.master("local") \
            .appName("Pearson Correlation of Price and Average Review Length") \
            .getOrCreate()

        self.price_ave_review_len_rdd = None
        self.pearson_correlation = 0.0

    def get_pearson_correlation(self):
        """
        :return: Pearson correlation of the latest uploaded books metadata and reviews
        """
        return self.pearson_correlation

    def get_price_and_average_review_length(self, books_metadata_path, book_reviews_path):
        """
        :param books_metadata_path: path to access book metadata
        :param book_reviews_path: path to access book reviews on Amazon
        :return: None
        """
        books_metadata = self.spark_session.read.json(books_metadata_path)

        book_asin_prices_raw = books_metadata.select('asin', 'price')
        book_asin_prices_cleaned = book_asin_prices_raw.filter(book_asin_prices_raw.price.isNotNull())

        book_reviews = self.spark_session.read.csv(book_reviews_path, header=True, mode="DROPMALFORMED")

        get_review_len = udf(lambda x: len(x.split(" ")) if x is not None else 0, IntegerType())
        book_ave_len = book_reviews.withColumn('review_len', get_review_len(book_reviews['reviewText'])) \
            .select('asin', 'review_len') \
            .groupby('asin') \
            .agg({'review_len': 'mean'})

        self.price_ave_review_len_rdd = book_asin_prices_cleaned.join(book_ave_len, "asin").rdd

    def calculate_pearson_correlation(self, decimals=10):
        """
        :param decimals: decimal place accuracy of pearson correlation. 10 dp by default
        :return: pearson correlation of price and average review length to {decimals} dp.
        """

        ave_len_price_prods = self.price_ave_review_len_rdd.map(lambda price_avg:
                                                                price_avg["price"] * price_avg["avg(review_len)"])
        sum_of_ave_len_price_prods = ave_len_price_prods.reduce(lambda val1, val2: val1 + val2)

        ave_lens = self.price_ave_review_len_rdd.map(lambda price_avg: price_avg["avg(review_len)"])
        sum_of_ave_lens = ave_lens.reduce(lambda val1, val2: val1 + val2)

        prices = self.price_ave_review_len_rdd.map(lambda price_avg: price_avg["price"])
        sum_of_prices = prices.reduce(lambda val1, val2: val1 + val2)

        ave_len_sq = self.price_ave_review_len_rdd.map(lambda price_avg: price_avg["avg(review_len)"] ** 2)
        sum_of_ave_len_sq = ave_len_sq.reduce(lambda val1, val2: val1 + val2)

        price_sq = self.price_ave_review_len_rdd.map(lambda price_avg: price_avg["price"] ** 2)
        sum_of_price_sq = price_sq.reduce(lambda val1, val2: val1 + val2)

        n = self.price_ave_review_len_rdd.count()

        numerator = n * sum_of_ave_len_price_prods - (sum_of_ave_lens * sum_of_prices)
        denominator = ((n * sum_of_price_sq - sum_of_prices ** 2) * (n * sum_of_ave_len_sq - sum_of_ave_lens ** 2))**.5

        pearson_correlation = round(numerator / denominator, decimals)

        return pearson_correlation

    def stop(self):
        """
        Stop the PearsonCorrelationCalculator
        """
        self.spark_session.stop()
        return

if __name__ == "__main__":
    DEFAULT_BOOK_METADATA_PATH = "hdfs:///databasegrp7/kindle-metadata-after-correction.json"
    DEFAULT_BOOK_REVIEWS_PATH = "hdfs:///databasegrp7/kindle_reviews.csv"

    pearson_correlation_calculator = PearsonCorrelationCalculator()

    pearson_correlation_calculator.get_price_and_average_review_length(DEFAULT_BOOK_METADATA_PATH,
                                                                    DEFAULT_BOOK_REVIEWS_PATH)

    pearson_correlation = pearson_correlation_calculator.calculate_pearson_correlation()
    pearson_correlation_calculator.stop()
    print('Pearson Correlation: ', pearson_correlation)
    
    with open('Pearson_output.txt','w') as file:
        file.write('Pearson Correlation: ')
        file.write(str(pearson_correlation))