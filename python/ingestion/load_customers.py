import pandas as pd
import snowflake.connector
from pathlib import Path
from snowflake.connector.pandas_tools import write_pandas

from python.utilities.config import SNOWFLAKE_CONFIG

# Read CSV
file_path = Path("datasets/customers.csv")
df = pd.read_csv(file_path)
df.columns = df.columns.str.upper() #snowflake is case sensitive, so we need to make sure the column names are in uppercase 

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=SNOWFLAKE_CONFIG["user"],
    password=SNOWFLAKE_CONFIG["password"],
    account=SNOWFLAKE_CONFIG["account"],
    warehouse=SNOWFLAKE_CONFIG["warehouse"],
    database=SNOWFLAKE_CONFIG["database"],
    schema=SNOWFLAKE_CONFIG["schema"],
    role=SNOWFLAKE_CONFIG["role"]
)

# Optional: clear existing data
conn.cursor().execute("TRUNCATE TABLE CUSTOMERS")

# Bulk load
success, nchunks, nrows, _ = write_pandas(
    conn,
    df,
    table_name="CUSTOMERS",
    auto_create_table=False
)

print(f"Success: {success}")
print(f"Chunks Loaded: {nchunks}")
print(f"Rows Loaded: {nrows}")

conn.close()