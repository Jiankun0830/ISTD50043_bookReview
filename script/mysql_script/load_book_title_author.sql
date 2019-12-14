-- create another table for scrapped info:
DROP TABLE IF EXISTS bookinfo;

CREATE TABLE bookinfo(
    asin CHAR(10),
    title text ,
    author text

);

load data local infile 'bookinfo.csv' 
into table bookinfo
fields terminated by ',' 
enclosed by '"' 
escaped by '"' 
lines terminated by '\r\n';


-- DELETE FROM book_author
-- where asin in 
-- (select asin from bookinfo)

-- Merge these 2 tables:

-- ALTER TABLE reviews
-- ADD COLUMN title text
-- AFTER asin;
-- ALTER TABLE reviews
-- ADD COLUMN author text
-- AFTER title;


-- UPDATE reviews t1
-- INNER JOIN bookinfo t2 ON t1.asin = t2.asin
-- SET t1.title = t2.title, t1.author = t2.author
-- ;


-- select idx,asin,title,author from reviews limit 10;

SELECT * FROM bookinfo
LIMIT 10;