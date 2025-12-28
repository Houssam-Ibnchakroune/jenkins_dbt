-- Simple sales table
CREATE TABLE IF NOT EXISTS sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT,
    sale_date DATE
);

-- Insert 5 simple records
INSERT INTO sales (product, price, quantity, sale_date) VALUES
('Laptop', 1000.00, 2, '2024-01-15'),
('Mouse', 25.50, 5, '2024-01-16'),
('Keyboard', 75.00, 3, '2024-01-17'),
('Monitor', 300.00, 1, '2024-01-18'),
('USB Cable', 10.00, 10, '2024-01-19');
