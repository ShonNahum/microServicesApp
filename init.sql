CREATE DATABASE IF NOT EXISTS user_service_db;

USE user_service_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    payment DECIMAL(10,2) DEFAULT 0.00
);
