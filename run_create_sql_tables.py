from modules.ExportDiscord import ExportDiscord
import json
import os
import glob
from dotenv import load_dotenv
load_dotenv()


ex_dis = ExportDiscord(os.environ.get("db_select"), os.environ.get("db_url"))
create_tables_status = ex_dis.create_sql_tables()
print(create_tables_status)
