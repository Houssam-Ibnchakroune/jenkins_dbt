-- Final: add simple category
SELECT 
    *,
    CASE 
        WHEN total_amount >= 100 THEN 'High Value'
        ELSE 'Low Value'
    END as value_category
FROM {{ ref('stg_sales') }}
