CREATE DATABASE ClothingStore;

USE ClothingStore;

CREATE TABLE clothes (
    clothID INT AUTO_INCREMENT PRIMARY KEY,
    style VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    brand VARCHAR(50) NOT NULL
);