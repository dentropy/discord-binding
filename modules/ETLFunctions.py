import logging
from datetime import datetime
import sys
import json
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

from modules.ExportDiscord import ExportDiscord
# from fix_schema_postgres import fix_schema_postgres

import boto3

# TODO Check all Environment Variables are valid, especially object_path_list

class ETLFunctions():
  now = datetime.now()
  formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
  folder_name = "./logs/"
  if not os.path.exists(folder_name):
      os.makedirs(folder_name)
      print(f"Folder '{folder_name}' created successfully!")
  else:
      print(f"Folder '{folder_name}' already exists.")
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f'{folder_name}/{formatted_date}-run_dag.log', 
    level=logging.INFO
  )
  logging.info("Starting Discord-to-SQL-Migration")

  def __init__(
    self,
    db_select,
    db_url,
    aws_access_key_id,
    aws_secret_access_key,
    endpoint_url
  ):
    self.db_url = db_url
    self.db_select = db_select
    self.aws_access_key_id = aws_access_key_id
    self.aws_secret_access_key = aws_secret_access_key
    self.endpoint_url = endpoint_url
    ex_dis = ExportDiscord(db_select, db_url)
    if(self.aws_access_key_id != "PLACEHOLDER"):
      self.s3_client = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key,
                      endpoint_url=endpoint_url
                      )
  def test_s3_connection(self):
    logging.info("Testing S3 Connection")
    try:
      buckets = self.s3_client.list_buckets()
    except Exception as e:
      logging.error("An error occurred:")
      logging.exception(e)
      logging.critical("S3 Connection is Invalid Exiting")
      sys.exit()
    logging.info("S3 connection is valid")

  def test_database_connection(self):
    logging.info("Testing Postgres Connection Connection")
    ex_dis = ExportDiscord(self.db_select, self.db_url)
    if ex_dis.test_connection() == True:
      logging.info("Postgres Connection is Valid")
    else:
      logging.critical("Postgres connection is invalid Exiting")
      sys.exit()


  def dump_list_s3_objects(self):
    logging.info("Getting list of S3 JSON objects")
    logging.debug("Checking for existing list of JSON object paths")
    try:
      self.s3_client = boto3.client('s3', 
        aws_access_key_id=os.environ.get("aws_access_key_id"), 
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
        endpoint_url=os.environ.get("endpoint_url")
      )
      json_object_paths = []
      paginator = self.s3_client.get_paginator('list_objects')
      operation_parameters = {'Bucket': os.environ.get("bucket_name") }
      page_iterator = paginator.paginate(**operation_parameters)
      for page in page_iterator:
          for obj in page["Contents"]:
              json_object_paths.append(obj["Key"])
              # if obj["Key"][-5:] == ".json" and "json_Files/" not in obj["Key"]:
              #   json_object_paths.append(obj["Key"])
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

  def get_list_s3_json_objects(self):
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
        self.s3_client = boto3.client('s3', 
          aws_access_key_id=os.environ.get("aws_access_key_id"), 
          aws_secret_access_key=os.environ.get("aws_secret_access_key"),
          endpoint_url=os.environ.get("endpoint_url")
        )
        json_object_paths = []
        paginator = self.s3_client.get_paginator('list_objects')
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

  def transform_s3_json_to_database_json(self, json_object_paths):
    logging.info("Transforming S3 JSON files to Postgres JSON")
    ex_dis = ExportDiscord(self.db_select, self.db_url)
    create_tables_status = ex_dis.create_raw_json_tables()
    for discord_object_json_path in json_object_paths:
      print("discord_object_json_path")
      pprint(discord_object_json_path)
      try:
        print("Getting Buckets")
        content_object = self.s3_client.get_object(
          Bucket=os.environ.get("bucket_name"),
          Key=discord_object_json_path
        )
        print("Got Bucket")
        mah_json = json.loads(  content_object["Body"].read().decode('utf-8')   )
        print("mah_json")
        processed_json = ex_dis.process_discord_json(mah_json)
        ex_dis.json_data_to_json_sql(processed_json)
        logging.info(f"Successfully Indexed: {discord_object_json_path}")
      except Exception as e:
        logging.debug(f"Error Reading S3 JSON Filename: {discord_object_json_path}")
        logging.debug(f"S3 JSON Error Description : {e}")
    logging.info("Successfully Transformed S3 JSON files to Postgres")

  def create_sql_tables(self):
    ex_dis = ExportDiscord(self.db_select, self.db_url)
    create_tables_status = ex_dis.create_sql_tables()

  def transform_s3_json_to_database_sql(self, json_object_paths):
    logging.info("Transforming S3 JSON files to Postgres SQL")
    ex_dis = ExportDiscord(self.db_select, self.db_url)
    create_tables_status = ex_dis.create_sql_tables()
    for discord_object_json_path in json_object_paths:
      print("discord_object_json_path")
      pprint(discord_object_json_path)
      try:
        print("Getting Buckets")
        content_object = self.s3_client.get_object(
          Bucket=os.environ.get("bucket_name"),
          Key=discord_object_json_path
        )
        mah_json = json.loads(  content_object["Body"].read().decode('utf-8')   )
        print("Got Bucket")
        processed_json = ex_dis.process_discord_json(mah_json)
        # pprint(processed_json)
        ex_dis.json_data_to_sql(processed_json)
        logging.info(f"Successfully Indexed: {discord_object_json_path}")
      except Exception as e:
        print("Error with S3 Object")
        pprint(e)
        logging.debug(f"Error Reading S3 JSON Filename: {discord_object_json_path}")
        logging.debug(f"S3 JSON Error Description : {e}")
    logging.info("Successfully Transformed S3 JSON files to Postgres")

  def transform_json_to_database_sql(self, json_object_paths):
    logging.info("Transforming JSON files to Postgres SQL")
    ex_dis = ExportDiscord(self.db_select, self.db_url)
    create_tables_status = ex_dis.create_sql_tables()
    for discord_object_json_path in json_object_paths:
      logging.info(f"discord_object_json_path {discord_object_json_path}")
      with open(discord_object_json_path, 'r') as json_file:
        try:
          mah_json = json.load(json_file)
          processed_json = ex_dis.process_discord_json(mah_json)
          ex_dis.json_data_to_sql(processed_json)
          logging.info(f"Successfully Indexed: {discord_object_json_path}")
        except Exception as e:
          print("Error with processing JSON file")
          pprint(e)
          logging.debug(f"Error Reading JSON Filename: {discord_object_json_path}")
          logging.debug(f"READ JSON Error Description : {e}")
        
        # For Testing
        # mah_json = json.load(json_file)
        # processed_json = ex_dis.process_discord_json(mah_json)
        # ex_dis.json_data_to_sql(processed_json)
        # logging.info(f"Successfully Indexed: {discord_object_json_path}")
    logging.info("Successfully Transformed JSON files to Postgres")
  # def transform_tables_in_database(self):
  #   fix_schema_postgres(os.environ.get("db_url"))