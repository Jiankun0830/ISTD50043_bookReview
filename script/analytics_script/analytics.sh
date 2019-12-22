wget https://database-project-50043.s3-us-west-2.amazonaws.com/kindle_reviews.csv
wget https://kindle-metadata.s3.amazonaws.com/kindle-metadata-after-correction.json
hdfs dfs -mkdir -p /databasegrp7
hdfs dfs -put kindle_reviews.csv /databasegrp7/kindle_reviews.csv
hdfs dfs -put kindle-metadata-after-correction.json /databasegrp7/kindle-metadata-after-correction.json
wget https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/analytics_script/pearson_cal.py
wget https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/analytics_script/tfidf_cal.py
sudo yum update
sudo yum install python-pip
sudo pip install numpy
python -m pip --no-cache-dir install pyspark --user
python pearson_cal.py
python tfidf_cal.py
hdfs dfs -get tfidf_output.csv ./tfidf
cd tfidf
cat * >> tfidf_output.csv
# path: ./tfidf/tfidf_output.csv
