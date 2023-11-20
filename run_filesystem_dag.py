from ETLFunctions import ETLFunctions
import json
import os
import glob
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

pprint("db_url")
pprint(os.environ.get("db_url"))

etl_functions = ETLFunctions(
  os.environ.get("db_select"),
  os.environ.get("db_url"),
  os.environ.get("aws_access_key_id"),
  os.environ.get("aws_secret_access_key"),
  os.environ.get("endpoint_url")
)
# etl_functions.test_database_connection()
directory_path = os.environ.get("discord_export_path")
from modules.find_json_files import find_json_files
json_file_paths = find_json_files(directory_path)
print(directory_path)
print(json_file_paths)
# json_file_paths = glob.glob(os.path.join(directory_path, '**/*.json')) # This did not work, waiting for future me to figure out why
etl_functions.transform_json_to_database_sql(json_file_paths)
