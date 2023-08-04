import os
import glob
from pprint import pprint
import sys
import json
# Directory where your JSON files are located
base_directory = "/home/paul/Projects/exports"

# Recursively find all JSON files in the directory and its subdirectories
json_files = glob.glob(os.path.join(base_directory, '**/*.json'), recursive=True)

dentropys_messages = {}
# Print the list of JSON files
pprint(json_files)
for json_file_path in json_files:
  with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)
  pprint(f"Importing {data['channel']['id']}")
  dentropys_messages[data["channel"]["id"]] = []
  for message in data["messages"]:
    if message["author"]["nickname"] == "dentropy":
      dentropys_messages[data["channel"]["id"]].append(message)
  pprint(f"Exported {data['channel']['id']}")

with open("out.json", 'w') as json_file:
    json.dump(dentropys_messages, json_file)

#  sys.exit()