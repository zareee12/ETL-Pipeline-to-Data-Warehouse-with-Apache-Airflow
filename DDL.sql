-- Skema: stg

-- Tabel: Sales
CREATE TABLE IF NOT EXISTS stg.Sales (
    SalesID INTEGER,
    SalesPersonID INTEGER,
    CustomerID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    Discount NUMERIC(6,2),
    TotalPrice NUMERIC(18,2),
    SalesDate DATE,
    TransactionNumber TEXT
);

-- Tabel: Categories
CREATE TABLE IF NOT EXISTS stg.Categories (
    CategoryID INTEGER,
    CategoryName TEXT
);

-- Tabel: Cities
CREATE TABLE IF NOT EXISTS stg.Cities (
    CityID INTEGER,
    CityName TEXT,
    Zipcode TEXT,
    CountryID INTEGER
);

-- Tabel: Countries
CREATE TABLE IF NOT EXISTS stg.Countries (
    CountryID INTEGER,
    CountryName TEXT,
    CountryCode TEXT
);

-- Tabel: Customers
CREATE TABLE IF NOT EXISTS stg.Customers (
    CustomerID INTEGER,
    FirstName TEXT,
    MiddleInitial TEXT,
    LastName TEXT,
    CityID INTEGER,
    Address TEXT
);

-- Tabel: Employee
CREATE TABLE IF NOT EXISTS stg.Employee (
    EmployeeID INTEGER,
    FirstName TEXT,
    MiddleInitial TEXT,
    LastName TEXT,
    BirthDate DATE,
    Gender TEXT,
    CityID INTEGER,
    HireDate TIMESTAMP
);

-- Tabel: Products
CREATE TABLE IF NOT EXISTS stg.Products (
    ProductID INTEGER,
    ProductName TEXT,
    Price NUMERIC(18,2),
    CategoryID INTEGER,
    Class TEXT,
    ModifyDate TIMESTAMP,
    Resistant TEXT,
    IsAllergic TEXT,
    VitalityDays TEXT
);

-- dimension table

CREATE TABLE IF NOT EXISTS dm.dim_product (
    sk_product SERIAL PRIMARY KEY,
    product_id INTEGER,
    product_name TEXT,
    product_price DECIMAL(18,2),
    category_id INTEGER,
    category_name TEXT,
    modify_datetime TIMESTAMP,
    insert_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS dm.dim_customer (
    sk_customer SERIAL PRIMARY KEY,
    customer_id INTEGER,
    customer_first_name TEXT,
    customer_middle_initial_name TEXT,
    customer_last_name TEXT,
    customer_address TEXT,
    customer_city_id INTEGER,
    customer_city_name TEXT,
    customer_zipcode TEXT,
    customer_country_id INTEGER,
    customer_country_name TEXT,
    customer_country_code TEXT,
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS dm.dim_employee (
    sk_employee SERIAL PRIMARY KEY,
    employee_id INTEGER,
    employee_first_name TEXT,
    employee_middle_initial TEXT,
    employee_last_name TEXT,
    employee_birth_date DATE,
    employee_gender TEXT,
    employee_city_id INTEGER,
    employee_city_name TEXT,
    employee_country_id INTEGER,
    employee_country_name TEXT,
    employee_country_code TEXT,
    employee_hire_date TIMESTAMP,
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS dm.dim_time (
    sk_date SERIAL PRIMARY KEY,
    date DATE,
    days VARCHAR(40),
    month_id INTEGER,
    month_name VARCHAR(40),
    year INTEGER
);

CREATE TABLE IF NOT EXISTS dm.fact_sales (
    sk_date INTEGER,
    sk_customer INTEGER,
    sk_employee INTEGER,
    sk_product INTEGER,
    sales_id INTEGER PRIMARY KEY,
    transaction_no TEXT,
    quantity DECIMAL(18, 2),
    discount DECIMAL(6, 2),
    total_price DECIMAL(18, 2),
    insert_date DATE DEFAULT CURRENT_DATE
);