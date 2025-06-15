transform_query = """
TRUNCATE TABLE dm.dim_product;

INSERT INTO dm.dim_product (
    product_id, product_name, product_price, category_id,
    category_name, modify_datetime, insert_date
)
SELECT 
    p.productid,
    p.productname,
    p.price,
    p.categoryid,
    c.categoryname,
    p.modifydate,
    CURRENT_DATE
FROM stg.products p
LEFT JOIN stg.categories c ON p.categoryid = c.categoryid;
"""