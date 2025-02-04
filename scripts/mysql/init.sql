CREATE DATABASE IF NOT EXISTS ClothingStore;

-- Create a new user
CREATE USER 'jason'@'%' IDENTIFIED BY 'ilovejason';

-- Grant all privileges on the new database to the user
GRANT ALL PRIVILEGES ON your_database.* TO 'jason'@'%';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;

USE ClothingStore;

CREATE TABLE clothes (
    clothID INT AUTO_INCREMENT PRIMARY KEY,
    style VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    brand VARCHAR(50) NOT NULL
);