import boto3
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()


s3_client = boto3.client('s3', 
                    aws_access_key_id=os.environ.get("aws_access_key_id"), 
                    aws_secret_access_key=os.environ.get("aws_secret_access_key"),
                    endpoint_url=os.environ.get("endpoint_url")
                    )

buckets = s3_client.list_buckets()

print("Listing All Bucket Names")
for bucket in buckets["Buckets"]:
    pprint(bucket["Name"])

# print("\nListing all items in first bucket")
# for obj in s3_client.list_objects(Bucket=  buckets["Buckets"][0]["Name"]  )['Contents']:
#     if obj["Key"][-5:] == ".json":
#       pprint(obj["Key"])

# pprint(len(
#   s3_client.list_objects(Bucket=  buckets["Buckets"][0]["Name"]  )
# ))

# data = s3_client.list_objects(Bucket=  buckets["Buckets"][0]["Name"]  )["Contents"]
# pprint(len(data))


# [Paginators - Boto3 1.28.60 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html#filtering-results)
json_object_paths = []
paginator = s3_client.get_paginator('list_objects')
operation_parameters = {'Bucket': buckets["Buckets"][0]["Name"] }
page_iterator = paginator.paginate(**operation_parameters)
for page in page_iterator:
    for obj in page["Contents"]:
        if obj["Key"][-5:] == ".json" and "json_Files/" not in obj["Key"]:
          print(obj["Key"])
          json_object_paths.append(obj["Key"])
print(len(json_object_paths))



BUCKET = 'InitalData'
FILE_TO_READ = "SET THIS.json"
content_object = s3_client.get_object(Bucket=BUCKET, Key=FILE_TO_READ)
mah_json = json.loads(  content_object["Body"].read().decode('utf-8')   )
pprint(mah_json)