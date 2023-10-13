#!/bin/bash

# Use the ls command to list files in the current directory
# You can replace "." with a specific directory path if needed
file_list=$(ls JupyterNotebooks/*ipynb)

# Loop through each file in the list
for file in $file_list; do
  # Perform actions on each file here
  echo "Processing file: $file"
  jupyter nbconvert --clear-output --inplace  $file
  # Add your custom commands here
done
# jupyter nbconvert --clear-output --inplace 