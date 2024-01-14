from pprint import pprint
import random
import os 
import time
import subprocess
import sys
from pathlib import Path
import json

if(len(sys.argv) == 3):
  print("First  Arg = output of run_S3_generate_index.py")
  print("Second Arg = List of paths you want to index")
  print("Third  Arg = Ouptut json file path")
  sys.exit()

input_path=sys.argv[1]
output_path=sys.argv[2]
output_path=sys.argv[3]

raw_paths = json.load(open(input_path))

guild_ids = json.load(open(input_path))
# guild_ids = ["748031363935895552", "612953348487905282", "902663358346571826", "484546513507188745", "810803176243724291", "858103637023391746"]

json_object_paths = []
for s3_path in raw_paths:
    for guild_id in guild_ids:
        if guild_id in s3_path and s3_path[-4:] == "json":
            print(f"Goe One: {s3_path}")
            json_object_paths.append(s3_path)




with open(output_path, "w") as json_file:
    json.dump(json_object_paths, json_file, indent=4)

