import os
import psycopg2


def reset_postgres_database(db_url):
  connection = psycopg2.connect(dsn = db_url)
  cursor = connection.cursor()
  print("Deleting Tables")
  # Get table names in the current schema
  cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
  tables = cursor.fetchall()

  # Drop each table
  for table in tables:
      table_name = table[0]
      drop_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
      cursor.execute(drop_query)
      print(f"Dropped table: {table_name}")

  # Commit the changes
  connection.commit()

  # Close communication with the PostgreSQL database
  cursor.close()
  connection.close()
  print("All tables dropped successfully!")
  print("Done Deleting Tables")