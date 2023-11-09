from ETLFunctions import ETLFunctions
import json
import os
from dotenv import load_dotenv
import glob
from pprint import pprint
load_dotenv()

pprint("TEST")
pprint(os.environ.get("db_url"))

etl_functions = ETLFunctions(
  os.environ.get("db_select"),
  os.environ.get("db_url"),
  os.environ.get("aws_access_key_id"),
  os.environ.get("aws_secret_access_key"),
  os.environ.get("endpoint_url")
)
etl_functions.test_database_connection()
directory_path = os.environ.get("discord_export_path")


import os
import fnmatch
def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.json'):
            json_files.append(os.path.join(root, filename))
    return json_files


json_file_paths = find_json_files(directory_path)
# json_file_paths = glob.glob(os.path.join(directory_path, '**/*.json')) # This did not work, waiting for future me to figure out why
etl_functions.transform_json_to_database_sql(json_file_paths)
