#!/bin/bash

sqlite_databases=$(find "$(pwd)"/out -type f)

for sqlite_path in $sqlite_databases; do
  echo "Migrating: $sqlite_path"
  python3 fix_schema.py $sqlite_path
done

echo "Done"