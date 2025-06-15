transform_query = """
TRUNCATE TABLE dm.dim_customer;

INSERT INTO dm.dim_customer (
            customer_id, customer_first_name, customer_middle_initial_name, 
            customer_last_name, customer_address, customer_city_id,
            customer_city_name, customer_zipcode, customer_country_id,
            customer_country_name, customer_country_code, start_date, end_date
        )
        SELECT 
            cu.customerid,
            cu.firstname,
            cu.middleinitial,
            cu.lastname,
            cu.address,
            cu.cityid,
            ci.cityname,
            ci.zipcode,
            ci.countryid,
            co.countryname,
            co.countrycode,
            CURRENT_DATE,
            NULL
        FROM stg.customers cu
        LEFT JOIN stg.cities ci ON cu.cityid = ci.cityid
        LEFT JOIN stg.countries co ON ci.countryid = co.countryid;
"""




