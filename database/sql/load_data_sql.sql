
CREATE DATABASE IF NOT EXISTS kindle_reviews;

USE kindle_reviews;

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews(
    idx INT,
    asin CHAR(10) NOT NULL,
    helpful text,
    overall INT,
    reviewText VARCHAR(8000),
    reviewTime text,
    reviewerID text,
    reviewerName text,
    summary text,
    unixReviewTime text

);


load data local infile 'kindle_reviews.csv' 
into table reviews
fields terminated by ',' 
enclosed by '"' 
escaped by '"' 
lines terminated by '\n'
ignore 1 lines;




SELECT * FROM reviews
LIMIT 10;