CREATE DATABASE IF NOT EXISTS ClothingStore;

-- Check if the user 'jason' exists before creating
SET @user_exists := (SELECT COUNT(*) FROM mysql.user WHERE user = 'jason' AND host = '%');

-- Create user only if it doesn't exist
SET @create_user_query := IF(@user_exists = 0, 'CREATE USER ''jason''@''%'' IDENTIFIED BY ''ilovejason''', 'SELECT "User already exists"');

PREPARE stmt FROM @create_user_query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON ClothingStore.* TO 'jason'@'%';

-- Apply changes
FLUSH PRIVILEGES;

USE ClothingStore;

CREATE TABLE IF NOT EXISTS clothes (
    clothID INT AUTO_INCREMENT PRIMARY KEY,
    style VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    brand VARCHAR(50) NOT NULL
);
