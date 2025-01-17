CREATE DATABASE ClothingStore;

USE ClothingStore;

CREATE TABLE clothes (
    clothID INT AUTO_INCREMENT PRIMARY KEY,
    style ENUM('athletic', 'casual', 'formal', 'business', 'sport', 'lounge') NOT NULL,
    color ENUM('Red', 'Green', 'Blue', 'Black', 'White', 'Yellow', 'Purple') NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    brand VARCHAR(50) NOT NULL
);