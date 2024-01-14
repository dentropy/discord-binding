from modules.ETLFunctions import ETLFunctions
import json
import os
import glob
import sys
from dotenv import load_dotenv
load_dotenv()

if(len(sys.argv) == 1):
  print("Input output of run_S3_generate_index.py")
  sys.exit()

etl_functions = ETLFunctions(
  os.environ.get("db_select"),
  os.environ.get("db_url"),
  os.environ.get("aws_access_key_id"),
  os.environ.get("aws_secret_access_key"),
  os.environ.get("endpoint_url")
)

etl_functions.test_s3_connection()
# etl_functions.test_database_connection()

json_object_paths = json.load(open(sys.argv[1]))
# json_object_paths = json.load(open('tmp_list.json', 'r'))
# json_object_paths = json.load(open('S3_JSON_OBJECTS.json', 'r'))
etl_functions.transform_s3_json_to_database_sql( json_object_paths )