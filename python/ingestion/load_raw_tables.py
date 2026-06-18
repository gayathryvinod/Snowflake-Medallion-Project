import pandas as pd
import snowflake.connector
from pathlib import Path
from snowflake.connector.pandas_tools import write_pandas

from python.utilities.config import SNOWFLAKE_CONFIG

conn = snowflake.connector.connect(
    user=SNOWFLAKE_CONFIG["user"],
    password=SNOWFLAKE_CONFIG["password"],
    account=SNOWFLAKE_CONFIG["account"],
    warehouse=SNOWFLAKE_CONFIG["warehouse"],
    database=SNOWFLAKE_CONFIG["database"],
    schema=SNOWFLAKE_CONFIG["schema"],
    role=SNOWFLAKE_CONFIG["role"]
)

def load_table(csv_path, table_name):
    df = pd.read_csv(csv_path)

    # Match Snowflake naming convention
    df.columns = df.columns.str.upper()

    conn.cursor().execute(f"TRUNCATE TABLE {table_name}")

    success, nchunks, nrows, _ = write_pandas(
        conn,
        df,
        table_name=table_name,
        auto_create_table=False
    )

    print(f"{table_name}: {nrows} rows loaded")

load_table("datasets/customers.csv", "CUSTOMERS")
load_table("datasets/orders.csv", "ORDERS")
load_table("datasets/order_items.csv", "ORDER_ITEMS")
load_table("datasets/products.csv", "PRODUCTS")
load_table("datasets/payments.csv", "PAYMENTS")
load_table("datasets/reviews.csv", "REVIEWS")
load_table("datasets/geolocation.csv", "GEOLOCATION")
load_table(
    "datasets/product_category_name_translation.csv",
    "PRODUCT_CATEGORY_NAME_TRANSLATION"
)

conn.close()