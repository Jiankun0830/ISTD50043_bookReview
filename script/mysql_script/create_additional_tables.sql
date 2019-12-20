use kindle_reviews;


-- 1. most rated books (top 20)
drop TABLE if EXISTS mostRated;

CREATE table if not EXISTS mostRated

select asin,avg(overall),count(distinct(reviewerID)) as rate_count
from reviews 
group by asin 
order by rate_count desc 
limit 20;

SELECT * FROM mostRated
LIMIT 10;


-- 2. highest rating score (top20)
drop TABLE if EXISTS highestAvgScore;

CREATE table if not EXISTS highestAvgScore

select asin,count(distinct(reviewerID)) as cnt,avg(overall) as avg_rating
from reviews
group by asin 
HAVING cnt > 4
order by avg_rating desc
limit 20;

SELECT * FROM highestAvgScore
LIMIT 10;