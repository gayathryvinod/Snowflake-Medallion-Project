import snowflake.connector
from config import SNOWFLAKE_CONFIG

conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
cur = conn.cursor()
cur.execute("SELECT CURRENT_VERSION()")
print(cur.fetchone())
cur.close()
conn.close()