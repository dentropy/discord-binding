#!/bin/bash

# Load .env variables
if [[ -f .env ]]; then
  source .env
else
  echo "The .env file does not exist."
  exit 1
fi


sqlite_databases=$(find "$(pwd)"/out -type f)

for sqlite_path in $sqlite_databases; do
  echo "Migrating: $sqlite_path"
  export sqlite_path=$sqlite_path
  export postgres_db_name=$postgres_db_name
  echo $sqlite_path
  echo $postgres_db_name
  envsubst < "db.load.template" > "db.load"
  pgloader db.load
  echo "Completed $sqlite_path"
  sleep 1
done

echo "Done"