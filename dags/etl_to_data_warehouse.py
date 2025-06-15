from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime
import os
import tempfile

import files.dim_customer as dc
import files.dim_employee as de
import files.dim_product as dp
import files.dim_time as dt
import files.fact_sales as fs

# Konstanta folder input
INPUT_FOLDER = '/opt/airflow/INPUT'

# Mapping file dan delimiter
TABLES = {
    "categories": ("categories", "|"),
    "cities": ("cities", ";"),
    "countries": ("countries", ";"),
    "customers": ("customers", ";"),
    "employes": ("employee", ";"),  # nama file employes.csv, tapi masuk ke table employee
    "products": ("products", ";"),
    "sales": ("sales", ";")
}

# Fungsi truncate
def truncate_table(table_name):
    pg_hook = PostgresHook(postgres_conn_id='data_warehouse_project')
    truncate_sql = f"TRUNCATE TABLE stg.{table_name};"
    pg_hook.run(truncate_sql)
    print(f"[INFO] Truncated table stg.{table_name}")

# Fungsi load csv
def load_csv_to_postgres(file_key, table_name, delimiter, execution_date_str):
    pg_hook = PostgresHook(postgres_conn_id='data_warehouse_project')

    folder_path = os.path.join(INPUT_FOLDER, execution_date_str)
    file_name = f"{execution_date_str}.{file_key}.csv"
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[ERROR] File tidak ditemukan: {file_path}")

    try:
        if table_name == "products":
            with open(file_path, 'r', encoding='utf-8') as original_file:
                lines = original_file.readlines()
            header = lines[0]
            cleaned_lines = [header]
            for line in lines[1:]:
                fields = line.strip().split(delimiter)
                if len(fields) >= 3:
                    fields[2] = fields[2].replace(",", ".")  # ubah hanya kolom Price
                cleaned_line = delimiter.join(fields) + "\n"
                cleaned_lines.append(cleaned_line)
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
                temp_file.writelines(cleaned_lines)
                temp_file_path = temp_file.name
        else:
            temp_file_path = file_path

        with open(temp_file_path, 'r', encoding='utf-8') as file:
            pg_hook.copy_expert(
                sql=f"COPY stg.{table_name} FROM STDIN WITH CSV DELIMITER '{delimiter}' HEADER;",
                filename=temp_file_path
            )
        print(f"[INFO] Berhasil load {file_name} ke stg.{table_name}")
    except Exception as e:
        raise RuntimeError(f"[ERROR] Gagal load {file_name}: {str(e)}")

# Default args DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 10),
    'retries': 1
}

with DAG(
    dag_id='etl_to_data_warehouse',
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    template_searchpath="/opt/airflow/dags/sql",
    tags=['ingestion', 'postgres', 'staging']
) as dag:

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    # Daftar task untuk didefinisikan dependencies-nya nanti
    truncate_tasks = []
    load_tasks = []

    for folder_date in ["20180508", "20180509"]:
        for file_key, (table_name, delimiter) in TABLES.items():
            truncate_task = PythonOperator(
                task_id=f"truncate_{table_name}_{folder_date}",
                python_callable=truncate_table,
                op_kwargs={"table_name": table_name}
            )

            load_task = PythonOperator(
                task_id=f"load_{table_name}_{folder_date}",
                python_callable=load_csv_to_postgres,
                op_kwargs={
                    "file_key": file_key,
                    "table_name": table_name,
                    "delimiter": delimiter,
                    "execution_date_str": folder_date
                }
            )

            truncate_tasks.append(truncate_task)
            load_tasks.append(load_task)

    # PENTING: Hubungkan masing-masing truncate ke load setelah semua task dibuat
    for t_task, l_task in zip(truncate_tasks, load_tasks):
        t_task >> l_task

    with TaskGroup(group_id="dim_group") as dim_group:
        dim_dc = SQLExecuteQueryOperator(
            task_id='dim_customer',
            conn_id='data_warehouse_project',
            sql=dc.transform_query
        )

        dim_de = SQLExecuteQueryOperator(
            task_id='dim_employee',
            conn_id='data_warehouse_project',
            sql=de.transform_query
        )   

        dim_dp = SQLExecuteQueryOperator(
            task_id='dim_product',
            conn_id='data_warehouse_project',
            sql=dp.transform_query
        )

        dim_dt = SQLExecuteQueryOperator(
            task_id='dim_time',
            conn_id='data_warehouse_project',
            sql=dt.transform_query
        )

    with TaskGroup(group_id="fact_group") as fact_group:
        fact_sales = SQLExecuteQueryOperator(
        task_id='fact_sales',
        conn_id='data_warehouse_project',
        sql=fs.transform_query
    )

    # ✅ Dependencies global (dengan perbaikan)
    start >> truncate_tasks
    for t_task, l_task in zip(truncate_tasks, load_tasks):
        t_task >> l_task
    load_tasks >> dim_group
    dim_group >> fact_group
    fact_group >> end
