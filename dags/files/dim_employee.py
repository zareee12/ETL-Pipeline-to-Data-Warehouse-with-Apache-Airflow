transform_query = """
TRUNCATE TABLE dm.dim_employee;

INSERT INTO dm.dim_employee (
            employee_id, employee_first_name, employee_middle_initial,
            employee_last_name, employee_birth_date, employee_gender,
            employee_city_id, employee_city_name, employee_country_id,
            employee_country_name, employee_country_code, employee_hire_date,
            start_date, end_date
        )
        SELECT 
            e.employeeid,
            e.firstname,
            e.middleinitial,
            e.lastname,
            e.birthdate,
            e.gender,
            e.cityid,
            ci.cityname,
            ci.countryid,
            co.countryname,
            co.countrycode,
            e.hiredate,
            CURRENT_DATE,
            NULL
        FROM stg.employee e
        LEFT JOIN stg.cities ci ON e.cityid = ci.cityid
        LEFT JOIN stg.countries co ON ci.countryid = co.countryid;
"""