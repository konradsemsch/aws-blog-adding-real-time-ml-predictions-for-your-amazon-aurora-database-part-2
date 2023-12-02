
import time
import pymysql
import random

import random
from decimal import Decimal

table_name = "mltest.churn_inserts"
schema = [
    ('state', 'VARCHAR(2)'),
    ('acc_length', 'INT'),
    ('area_code', 'INT'),
    ('phone', 'VARCHAR(10)'),
    ('int_plan', 'VARCHAR(3)'),
    ('vmail_plan', 'VARCHAR(3)'),
    ('vmail_msg', 'INT'),
    ('day_mins', 'FLOAT'),
    ('day_calls', 'INT'),
    ('day_charge', 'FLOAT'),
    ('eve_mins', 'FLOAT'),
    ('eve_calls', 'INT'),
    ('eve_charge', 'FLOAT'),
    ('night_mins', 'FLOAT'),
    ('night_calls', 'INT'),
    ('night_charge', 'FLOAT'),
    ('int_mins', 'FLOAT'),
    ('int_calls', 'INT'),
    ('int_charge', 'FLOAT'),
    ('cust_service_calls', 'INT')
]

def generate_random_phone_number():
    area_code = random.randint(100, 999)
    phone_number = random.randint(1000, 9999)
    phone_number_str = f'{area_code:03d}-{phone_number:04d}'
    return f"'{phone_number_str}'"

def generate_random_sql_insert(table_name, schema):
    columns = [col[0] for col in schema]
    data_types = [col[1] for col in schema]
    
    state_abbreviations = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
        'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
        'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
        'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]

    # Generate random values based on data types
    values = []
    for data_type in data_types:
        if data_type == 'VARCHAR(2)':
            value = f"'{random.choice(state_abbreviations)}'"
        elif data_type == 'INT':
            value = random.randint(1, 100)
        elif data_type == 'FLOAT':
            value = round(random.uniform(1, 100), 2)
        elif data_type == 'DECIMAL':
            value = round(Decimal(random.uniform(1, 100)), 2)
        elif data_type == 'VARCHAR(3)':
            value = random.choice(["'yes'", "'no'"])
        elif data_type == 'VARCHAR(10)':
            value = generate_random_phone_number()
        else:
            value = None  # Handle other data types as needed
        
        values.append(str(value) if value is not None else 'NULL')
    
    columns = ', '.join(columns)
    values = ', '.join(values)
    
    sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
    
    return sql_insert

if __name__ == "__main__":

    conn = pymysql.connect(
        host="<WRITER ENDPOINT>", 
        port=3306, 
        user="<USER>", 
        password="<PASSWORD>"
        )

    n_requests = int(random.uniform(0.5, 1)*1000)
    print(f"N requests: {n_requests}")
    for i in range(n_requests):
        time.sleep(random.uniform(0, 1))
        try:
            with conn.cursor() as cursor:
                statement = generate_random_sql_insert(table_name, schema)
                print(f"Executing statement: {statement}")
                cursor.execute(f"{statement};")
                print("Done")
            conn.commit()
    
        except Exception as error:
            print("Error connecting to MySQL database: {}".format(error))

    conn.close()