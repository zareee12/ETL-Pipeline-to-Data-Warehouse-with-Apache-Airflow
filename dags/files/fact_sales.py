transform_query = """
TRUNCATE TABLE dm.fact_sales;

INSERT INTO dm.fact_sales (
    sk_date,
    sk_customer,
    sk_employee,
    sk_product,
    sales_id,
    transaction_no,
    quantity,
    discount,
    total_price,
    insert_date
)
SELECT DISTINCT ON (s.salesid)
    d.sk_date,
    c.sk_customer,
    e.sk_employee,
    p.sk_product,
    s.salesid,
    s.transactionnumber,
    s.quantity,
    s.discount,
    s.totalprice,
    CURRENT_DATE
FROM stg.sales s
LEFT JOIN dm.dim_time d ON s.salesdate = d.date
LEFT JOIN dm.dim_customer c ON s.customerid = c.customer_id
LEFT JOIN dm.dim_employee e ON s.salespersonid = e.employee_id
LEFT JOIN dm.dim_product p ON s.productid = p.product_id
ORDER BY s.salesid, s.transactionnumber;
"""
