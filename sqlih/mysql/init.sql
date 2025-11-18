CREATE DATABASE IF NOT EXISTS ctfdb;
USE ctfdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS flag (
    flag VARCHAR(255) NOT NULL
);

-- normal user (benign)
INSERT INTO users (username, password) VALUES ('guest', 'guest123');

-- admin account. Password is unknown to players.
INSERT INTO users (username, password) VALUES ('admin', 'verysecret');

-- flag for admin
INSERT INTO flag (flag) VALUES ('flag{nonono}');
