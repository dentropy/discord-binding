import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
load_dotenv()


create_table_queries = [

"""
CREATE TABLE IF NOT EXISTS guilds_t (
  id          INTEGER PRIMARY KEY,
  guild_id    TEXT,
  guild_name  TEXT,
  iconUrl     TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS channels_t (
  id            INTEGER PRIMARY KEY,
  channel_name  TEXT,
  channel_type  TEXT,
  categoryId    TEXT,
  category      TEXT,
  guild_id      INTEGER,
  topic         TEXT,
  channel_name_length INT,
  FOREIGN KEY (guild_id) REFERENCES guilds_t(id)
)
""",

"""
CREATE TABLE IF NOT EXISTS messages_t (
  id           INTEGER PRIMARY KEY,
  attachments  TEXT,
  author       TEXT,
  channel_id   INTEGER,
  content      TEXT,
  interaction  TEXT,
  isBot        BOOLEAN,
  isPinned     BOOLEAN,
  mentions     BOOLEAN,
  msg_type     TEXT,
  timestamp    INT,
  timestampEdited INT,
  content_length INT,
  FOREIGN KEY (channel_id) REFERENCES channels_t(id)
)
""",


"""
CREATE TABLE IF NOT EXISTS authors_t (
  id            INTEGER PRIMARY KEY,
  author_id     INTEGER,
  name          TEXT,
  nickname      TEXT,
  color         TEXT,
  isBot         BOOLEAN,
  avatarUrl     TEXT
)
""",


"""
CREATE TABLE IF NOT EXISTS attachments_t (
  id                    INTEGER PRIMARY KEY,
  attachment_url        TEXT,
  attachment_filename   TEXT,
  fileSizeBytes         INTEGER,
  message_id            INTEGER
)
""",

"""
CREATE TABLE IF NOT EXISTS roles_t (
  id          INTEGER PRIMARY KEY,
  role_name   TEXT,
  color       TEXT,
  position    INTEGER
)
""",

]

try:
    url = urlparse(os.environ.get("postgres_url"))
    print(url)
    conn = psycopg2.connect(
        host=url.hostname,
        port=url.port,
        database=url.path[1:],
        user=url.username,
        password=url.password
    )
    cursor = conn.cursor()
    for query in create_table_queries:
      cursor.execute(query)
      conn.commit()
      print("Another table created")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")