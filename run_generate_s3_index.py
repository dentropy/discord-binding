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

json_object_paths = etl_functions.dump_list_s3_objects()
with open("Export it All Yo2" + ".json", "w") as json_file:
    json.dump(json_object_paths, json_file, indent=4)
# json_object_paths = json.load(open('tmp_list.json', 'r'))
# json_object_paths = json.load(open('S3_JSON_OBJECTS.json', 'r'))
# etl_functions.transform_s3_json_to_database_sql( json_object_paths )