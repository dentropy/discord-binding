import os
import fnmatch
def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.json'):
            json_files.append(os.path.join(root, filename))
    return json_files