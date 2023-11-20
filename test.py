import pytest
from pprint import pprint
import os
import sys
from dotenv import load_dotenv
load_dotenv()

from modules.reset_db        import reset_postgres_database
from modules.find_json_files import find_json_files

def test_db_connection():
  from ExportDiscord import ExportDiscord
  ex_dis = ExportDiscord(
    os.environ.get("db_select"),
    os.environ.get("db_url")
  )
  result = ex_dis.test_connection()
  print(result)
  assert result == True

def test_schema_creation():
  from ExportDiscord import ExportDiscord
  ex_dis = ExportDiscord(
    os.environ.get("db_select"),
    os.environ.get("db_url")
  )
  create_tables_status = ex_dis.create_sql_tables()

def test_schema_creation_and_reset():
  from ExportDiscord import ExportDiscord
  ex_dis = ExportDiscord(
    os.environ.get("db_select"),
    os.environ.get("db_url")
  )
  create_tables_status = ex_dis.create_sql_tables()
  import psycopg2
  conn = psycopg2.connect(dsn = os.environ.get("db_url") )
  cursor = conn.cursor()
  cursor.execute("SELECT current_schema();")
  current_schema = cursor.fetchone()[0]
  query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{current_schema}' AND table_type = 'BASE TABLE';"
  cursor.execute(query)
  tables_count = cursor.fetchone()[0]
  assert tables_count >= 8
  reset_postgres_database(os.environ.get("db_url"))
  query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{current_schema}' AND table_type = 'BASE TABLE';"
  cursor.execute(query)
  tables_count = cursor.fetchone()[0]
  pprint(tables_count)
  assert tables_count == 0

def test_indexing_json_file(discord_object_json_path):
  import json
  from ExportDiscord import ExportDiscord
  ex_dis = ExportDiscord(
    os.environ.get("db_select"),
    os.environ.get("db_url")
  )
  create_tables_status = ex_dis.create_sql_tables()
  try:
    with open(discord_object_json_path, 'r') as json_file:
      pprint(json_file)
      mah_json = json.load(json_file)
  except Exception as e:
      print(f"Failed process_json_file, json.load {discord_object_json_path}")
      pprint(e)
      sys.exit()
  try:
      processed_json = ex_dis.process_discord_json(mah_json)
  except Exception as e:
    print("Failed process_json_file, ex_dis.process_discord_json ")
    pprint(e)
    sys.exit()
  ex_dis.json_data_to_sql(processed_json)
  try: 
    ex_dis.json_data_to_sql(processed_json)
  except Exception as e:
    print("Failed process_json_file, ex_dis.json_data_to_sql ")
    pprint(e)
    sys.exit()
  # reset_postgres_database(os.environ.get("db_url"))


def test_sqlalchemy_schema_creation():
  import os
  from sqlalchemy import create_engine
  from sqlalchemy.orm import Session

  from schema_sqlalchemy import Base 

  engine_path = os.environ.get("db_url")
  engine = create_engine(os.environ.get("db_url"), echo=True)


  Base.metadata.create_all(engine) 
  session = Session(engine)

# test_db_connection()
# test_schema_creation()
# test_schema_creation_and_reset()
# reset_postgres_database(os.environ.get("db_url"))
directory_path = os.environ.get("discord_export_path")
json_file_paths = find_json_files(directory_path)
test_indexing_json_file(json_file_paths[0])
