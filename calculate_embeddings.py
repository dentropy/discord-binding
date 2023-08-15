# The Plan

# Create New Tables for Embeddings
# Create a loop to go through the messages
  # Check if Message is in new tableTable before Calculating Embedding
  # Calculate Embedding
  # Save embedding to table
  # Sleep a second

import sqlite3
import time
import cohere
import json

import os
from dotenv import load_dotenv
load_dotenv()

co = cohere.Client(os.getenv('COHERE_API_KEY')) # This is your trial API key

# Create New Tables for Embeddings
sqlite_url = os.getenv('sqlite_url')
con = sqlite3.connect(sqlite_url)
cursor = con.cursor()
# cursor.execute("DROP TABLE cohere_embeddings_t").fetchall()
create_table_query = f'''
    CREATE TABLE IF NOT EXISTS cohere_embeddings_t (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id       VARCHAR,
        message_contents TEXT,
        raw_embedding    TEXT
    )
'''
cursor.execute(create_table_query).fetchall()

# Create a loop to go through the messages
# Define the batch size (number of rows to fetch at a time)
batch_size = 10
# Initial offset to keep track of where we are in the table
offset = 0
while True:
    # Query to fetch the next batch of rows
    query = f"""
      SELECT
        json_extract(raw_messages_t.raw_json, '$.id') as message_id,
        json_extract(raw_messages_t.raw_json, '$.content') as content
      FROM raw_messages_t 
      LIMIT {batch_size} 
      OFFSET {offset}
    """
    cursor.execute(query)
    batch_rows = cursor.fetchall()
    if not batch_rows:
        # No more rows to fetch, exit the loop
        break
    # Process the current batch of rows
    for row in batch_rows:
        # Check if Message is in new tableTable before Calculating Embedding
        query = f"""
              SELECT
                COUNT(*)
              FROM cohere_embeddings_t 
              WHERE message_id = '{row[0]}'
            """
        print(row)  # You can replace this with your desired processing logic
        check_in_table = cursor.execute(query).fetchall()
        if(check_in_table[0][0] == 0):
            if  len(row[1]) < 7:
                # SQL INSERT statement
                insert_query = "INSERT INTO cohere_embeddings_t (message_id, message_contents) VALUES (?, ?)"
                cursor.execute(insert_query, (row[0], row[1])).fetchall()
            else:
                # time.sleep(3)
                # Calculate Embedding
                response = co.embed(
                  model='embed-english-v2.0',
                  texts=[row[1]])
                insert_query = "INSERT INTO cohere_embeddings_t (message_id, message_contents, raw_embedding) VALUES (?, ?, ?)"
                cursor.execute(insert_query, (row[0], row[1], str(response.embeddings))).fetchall()
                con.commit()
                # Save embedding to table
                # Sleep a second
                time.sleep(1)
    # Increment the offset for the next batch
    offset += batch_size
# Close the database connection
conn.close()
