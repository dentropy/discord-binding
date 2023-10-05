import logging
from datetime import datetime
import sys
import boto3

import os
from dotenv import load_dotenv
load_dotenv()

from ExportDiscord import ExportDiscord

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  filename=f'{formatted_date}-run_dag.log', 
  level=logging.INFO
)
logging.debug("Starting Discord-to-SQL-Migration")


logging.debug("Testing S3 Connection")
try:
  s3_client = boto3.client('s3', 
                      aws_access_key_id=os.environ.get("aws_access_key_id"), 
                      aws_secret_access_key=os.environ.get("aws_secret_access_key"),
                      endpoint_url=os.environ.get("endpoint_url")
                      )
  buckets = s3_client.list_buckets()
except Exception as e:
  logger.error("An error occurred:")
  logger.exception(e)
  logging.critical("S3 Connection is Invalid Exiting")
  sys.exit()
logging.debug("S3 connection is valid")



logging.debug("Testing Postgres Connection Connection")
ex_dis = ExportDiscord(  
  os.environ.get("db_select"),
  os.environ.get("db_url")  
)
if ex_dis.test_connection() == True:
  logging.debug("Postgres Connection is Valid")
else:
  logging.critical("Postgres connection is invalid Exiting")
  sys.exit()



logging.debug("Getting list of JSON objects")
try:
  json_object_paths = []
  paginator = s3_client.get_paginator('list_objects')
  operation_parameters = {'Bucket': os.environ.get("bucket_name") }
  page_iterator = paginator.paginate(**operation_parameters)
  for page in page_iterator:
      for obj in page["Contents"]:
          if obj["Key"][-5:] == ".json" and "json_Files/" not in obj["Key"]:
            print(obj["Key"])
            json_object_paths.append(obj["Key"])
  print(len(json_object_paths))
except Exception as e:
  logger.error("An error occurred:")
  logger.exception(e)
  logging.critical("Unable to get list of JSON objects, Exiting")
  sys.exit()
