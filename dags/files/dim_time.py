transform_query = """
TRUNCATE TABLE dm.dim_time;

INSERT INTO dm.dim_time(date, days, month_id, month_name, year)
SELECT 
days.d::DATE as date, 
to_char(days.d, 'FMMonth DD, YYYY') as days, 
to_char(days.d, 'MM')::integer as month_id, 
to_char(days.d, 'FMMonth') as month_name, 
to_char(days.d, 'YYYY')::integer as year
from (
    SELECT generate_series(
        ('2000-01-01')::date, -- 'start' date
        ('2100-12-31')::date, -- 'end' date
        interval '1 day'  -- one for each day between the start and day
        )) as days(d);
"""