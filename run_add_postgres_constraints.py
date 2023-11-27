from schemas.schema_postgres import constraint_queries
from dotenv import load_dotenv
from pprint import pprint
import os
import psycopg2
load_dotenv()

pprint(os.environ.get("db_url"))

for query in constraint_queries:
    try:
        con = psycopg2.connect(dsn=os.environ.get("db_url"))
        cur = con.cursor()
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(f"SQL Query Failed, \n{query}")