CREATE DATABASE IF NOT EXISTS accounts_info;

USE accounts_info;

DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL,
    isadmin Boolean NOT NULL
);