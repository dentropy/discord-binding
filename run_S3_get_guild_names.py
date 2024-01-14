from modules.ETLFunctions import ETLFunctions
import json
import os
import glob
import boto3
from pprint import pprint
import sys
from dotenv import load_dotenv
load_dotenv()

if(len(sys.argv) == 2):
  print("First Arg = Input Filename, Second Arg = Output Filename")
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


# We remove anything that is not a JSON file
list_json_files = []
for file in json_object_paths:
    if file[-4:] == "json":
        list_json_files.append(file)


# We group all the JOSN into their root folder
folder_json_files = {}
for file in list_json_files:
    file_split = file.split("/")
    file_join = "/".join(file_split[1:])
    if file_split[0] not in folder_json_files.keys():
        folder_json_files[file_split[0]] = [ file ]
    else:
        folder_json_files[file_split[0]].append(file)
pprint(folder_json_files)


s3_client = boto3.client('s3', 
        aws_access_key_id=os.environ.get("aws_access_key_id"), 
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
        endpoint_url=os.environ.get("endpoint_url")
      )


# We loop through the JSON files until we get a guild_name
guild_export_json = {}
for guild in folder_json_files.keys():
    for object_path in folder_json_files[guild]:
        try:
            content_object = s3_client.get_object(
                Bucket=os.environ.get("bucket_name"),
                Key=object_path
            )
            mah_json = json.loads(  content_object["Body"].read().decode('utf-8')   )
            if "guild" in mah_json.keys():
                print("\nGot a Guild")
                guild_export_json[mah_json["guild"]["name"]] = mah_json["guild"]["id"]
                print(mah_json["guild"]["name"])
                print(mah_json["guild"]["id"])
                break 
        except Exception as error:
            print(error)

with open(sys.argv[2], 'w') as f:
    json.dump(guild_export_json, open(sys.argv[2], 'w'))
# Save file data structure