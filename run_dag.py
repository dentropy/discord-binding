import logging
from datetime import datetime
import sys
import json
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

from ExportDiscord import ExportDiscord
from fix_schema_postgres import fix_schema_postgres

import boto3

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  filename=f'{formatted_date}-run_dag.log', 
  level=logging.INFO
)
logging.info("Starting Discord-to-SQL-Migration")

# TODO Check all Environment Variables are valid, especially object_path_list

def test_s3_connection():
  logging.info("Testing S3 Connection")
  try:
    buckets = s3_client.list_buckets()
  except Exception as e:
    logging.error("An error occurred:")
    logging.exception(e)
    logging.critical("S3 Connection is Invalid Exiting")
    sys.exit()
  logging.info("S3 connection is valid")

def test_database_connection():
  logging.info("Testing Postgres Connection Connection")
  if ex_dis.test_connection() == True:
    logging.info("Postgres Connection is Valid")
  else:
    logging.critical("Postgres connection is invalid Exiting")
    sys.exit()


def get_list_s3_json_objects():
  logging.info("Getting list of S3 JSON objects")
  logging.debug("Checking for existing list of JSON object paths")
  if(  os.environ.get("object_path_list") != "" and os.environ.get("save_new_object_path_list") != "True" ):
    try:
        # Attempt to open and load the JSON file
        with open(os.environ.get("object_path_list"), 'r') as file:
            data = json.load(file)
        # At this point, 'data' contains the parsed JSON data
        logging.debug("JSON file loaded successfully.")
        return data
    except FileNotFoundError:
        object_path_list = os.environ.get("object_path_list")
        logging.debug(f"File not found: {object_path_list}")
    except json.JSONDecodeError as e:
        logging.debug(f"JSON decoding error: {e}")
    except Exception as e:
        logging.debug(f"An unexpected error occurred: {e}")
  else:
    logging.debug("No JSON object paths file found ")
    try:
      s3_client = boto3.client('s3', 
        aws_access_key_id=os.environ.get("aws_access_key_id"), 
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
        endpoint_url=os.environ.get("endpoint_url")
      )
      json_object_paths = []
      paginator = s3_client.get_paginator('list_objects')
      operation_parameters = {'Bucket': os.environ.get("bucket_name") }
      page_iterator = paginator.paginate(**operation_parameters)
      for page in page_iterator:
          for obj in page["Contents"]:
              if obj["Key"][-5:] == ".json" and "json_Files/" not in obj["Key"]:
                json_object_paths.append(obj["Key"])
                print(obj["Key"])
      logging.debug(f"Length of JSON files = {len(json_object_paths)}")
    except Exception as e:
      logging.error("An error occurred:")
      logging.exception(e)
      logging.critical("Unable to get list of JSON objects, Exiting")
      sys.exit()
  if os.environ.get("save_new_object_path_list") == "True":
    with open(os.environ.get("object_path_list"), "w") as json_file:
      json.dump(json_object_paths, json_file, indent=4)
  logging.info("Successfully got list of S3 JSON objects")
  return json_object_paths

def transform_s3_json_to_database(json_object_paths):
  logging.info("Transforming S3 JSON files to Postgres")
  create_tables_status = ex_dis.create_raw_json_tables()
  for discord_object_json_path in json_object_paths:
    print("discord_object_json_path")
    print(discord_object_json_path)
    try:
      print("Getting Buckets")
      content_object = s3_client.get_object(
        Bucket=os.environ.get("bucket_name"),
        Key=discord_object_json_path
      )
      mah_json = json.loads(  content_object["Body"].read().decode('utf-8')   )
      print("mah_json")
      processed_json = ex_dis.process_discord_json(mah_json)
      ex_dis.json_data_to_sql(processed_json)
      logging.info(f"Successfully Indexed: {discord_object_json_path}")
    except Exception as e:
      logging.debug(f"Error Reading S3 JSON Filename: {discord_object_json_path}")
      logging.debug(f"S3 JSON Error Description : {e}")
  logging.info("Successfully Transformed S3 JSON files to Postgres")



def transform_tables_in_database():
  fix_schema_postgres(os.environ.get("db_url"))


s3_client = boto3.client('s3', 
                    aws_access_key_id=os.environ.get("aws_access_key_id"), 
                    aws_secret_access_key=os.environ.get("aws_secret_access_key"),
                    endpoint_url=os.environ.get("endpoint_url")
                    )
ex_dis = ExportDiscord(  
  os.environ.get("db_select"),
  os.environ.get("db_url")  
)
test_s3_connection()
test_database_connection()
json_object_paths = get_list_s3_json_objects()
for json_object_path in json_object_paths:
  print(json_object_path)
transform_s3_json_to_database( json_object_paths )
transform_tables_in_database()
