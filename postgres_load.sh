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
  sqlite3 $sqlite_path -csv "SELECT * FROM guilds_t;" > guilds_t.csv
  psql $postgres_url -c "\copy guilds_t FROM '$(pwd)/guilds_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed guilds_t for $sqlite_path"
  sqlite3 $sqlite_path -csv "SELECT * FROM channels_t;" > channels_t.csv
  psql $postgres_url -c "\copy channels_t FROM '$(pwd)/channels_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed channels_t for $sqlite_path"
  sqlite3 $sqlite_path -csv "SELECT * FROM messages_t;" > messages_t.csv
  psql $postgres_url -c "\copy messages_t FROM '$(pwd)/messages_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed messages_t for $sqlite_path"
  sqlite3 $sqlite_path -csv "SELECT * FROM authors_t;" > authors_t.csv
  psql $postgres_url -c "\copy authors_t FROM '$(pwd)/authors_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed authors_t for $sqlite_path"
  sleep 1
done

echo "Done"