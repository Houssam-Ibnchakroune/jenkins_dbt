-- Staging: just select data
SELECT 
    id,
    product,
    price,
    quantity,
    sale_date,
    total_amount
FROM raw_data
WHERE price > 0 AND quantity > 0
