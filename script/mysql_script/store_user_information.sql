CREATE DATABASE IF NOT EXISTS accounts_info;

USE accounts_info;

DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL,
    isadmin Boolean NOT NULL
);


INSERT INTO accounts(username,password,isadmin)
VALUES
('Ainul', MD5('123456'),1),
('Jiankun', MD5('123456'),1),
('Pengfei', MD5('123456'),1),
('Yunyi', MD5('123456'),1),
('Shanshan', MD5('123456'),1),
('Nashita', MD5('123456'),1),
('Lutong', MD5('123456'),1),
('test1',MD5('123456'),0)
;

SELECT * FROM accounts
LIMIT 10;