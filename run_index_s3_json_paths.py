from modules.ETLFunctions import ETLFunctions
import json
import os
import glob
from dotenv import load_dotenv
load_dotenv()


etl_functions = ETLFunctions(
  os.environ.get("db_select"),
  os.environ.get("db_url"),
  os.environ.get("aws_access_key_id"),
  os.environ.get("aws_secret_access_key"),
  os.environ.get("endpoint_url")
)

etl_functions.test_s3_connection()
# etl_functions.test_database_connection()

json_object_paths = json.load(open('index_me.json'))
# json_object_paths = json.load(open('tmp_list.json', 'r'))
# json_object_paths = json.load(open('S3_JSON_OBJECTS.json', 'r'))
etl_functions.transform_s3_json_to_database_sql( json_object_paths )