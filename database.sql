CREATE DATABASE IF NOT EXISTS car_parking;

USE car_parking;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_number VARCHAR(20) UNIQUE NOT NULL,
    owner_name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parking_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    car_number VARCHAR(20) NOT NULL,
    checkin_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    checkin_time TIME NOT NULL,
    checkout_time TIME NOT NULL,
    parking_plan VARCHAR(20) NOT NULL,
    rent_amount DECIMAL(10,2) NOT NULL,
    spot_images TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);