import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer

os.environ["PYSPARK_PYTHON"] = "/usr/bin/python"
session = SparkSession.builder.master("local").appName('tfidf').getOrCreate()
reviews = session.read.options(header=True).csv("hdfs:///databasegrp7/kindle_reviews.csv")
reviews = reviews.na.fill({'reviewText': ''})
tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
wordsData = tokenizer.transform(reviews)
cv = CountVectorizer(inputCol="words", outputCol="rawFeatures")
model = cv.fit(wordsData)
feature_data = model.transform(wordsData)
idf = IDF(inputCol="rawFeatures", outputCol="features")
idf_model = idf.fit(feature_data)
rescaled_data = idf_model.transform(feature_data)
rescaled_data.select("features").show()
vocab = model.vocabulary


def extract_values(vector):
    return {vocab[i]: float(tfidf) for (i, tfidf) in zip(vector.indices, vector.values)}


def save_as_string(vector):
    words = ""
    for (i, tfidf) in zip(vector.indices, vector.values):
        temp = vocab[i] + ":" + str(float(tfidf)) + ", "
        words += temp
    return words[:-2]


output = rescaled_data.select('reviewerID', 'asin', 'reviewTime', 'features').rdd.map(
    lambda x: [x[0], x[1], x[2], save_as_string(x[3])])
output_df = session.createDataFrame(output, ['reviewerID', 'asin', 'reviewTime', 'tfidf'])
output_df.write.csv('tfidf_output.csv')
session.stop()
