#!/bin/bash

# Load .env variables
if [[ -f .env ]]; then
  source .env
else
  echo "The .env file does not exist."
  exit 1
fi
export sqlite_path=$sqlite_path
export postgres_db_name=$postgres_db_name
export postgres_url=$postgres_url

python3 postgres_schema.py

sqlite_databases=$(find "$(pwd)"/out -type f)

for sqlite_path in $sqlite_databases; do
  echo "Migrating: $sqlite_path"
  export sqlite_path=$sqlite_path
  export postgres_db_name=$postgres_db_name
  export postgres_url=$postgres_url
  echo $sqlite_path
  echo $postgres_db_name
  echo $postgres_url
  sqlite3 $sqlite_path -csv "SELECT * FROM guilds_t;" > guilds_t.csv
  psql $postgres_url -c "\copy guilds_t FROM '$(pwd)/guilds_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed guilds_t for $sqlite_path"
  sqlite3 $sqlite_path -csv "SELECT * FROM channels_t;" > channels_t.csv
  psql $postgres_url -c "\copy channels_t FROM '$(pwd)/channels_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed channels_t for $sqlite_path"
  sqlite3 $sqlite_path -csv "SELECT * FROM messages_t;" > messages_t.csv
  psql $postgres_url -c "\copy messages_dump_t FROM '$(pwd)/messages_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed messages_t for $sqlite_path"
  sqlite3 $sqlite_path -csv "SELECT * FROM authors_t;" > authors_t.csv
  psql $postgres_url -c "\copy authors_dump_t FROM '$(pwd)/authors_t.csv'  WITH (FORMAT CSV, HEADER false);"
  echo "Completed authors_dump_t for $sqlite_path"
  sleep 1
done
echo "putting data inside authors_t"
psql $postgres_url -c "insert into authors_t (id, author_id, name, nickname, color, isBot, avatarurl) ( select id, author_id, name, nickname, color, isBot, avatarurl from authors_dump_t ) on conflict (id) do nothing;"
# psql $postgres_url -c "INSERT INTO messages_t ( id, channel_id, attachments, author, content, interaction, ispinned, mentions, msg_type, timestamp, timestampedited, content_length ) ( select id, channel_id, attachments, author, content, interaction, ispinned, mentions, msg_type, To_timestamp(timestamp), To_timestamp(timestampedited), content_length FROM messages_dump_t ) on conflict ( id ) do nothing;"
echo "Done"