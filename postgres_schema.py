import psycopg2
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()


create_table_queries = [

"""
CREATE TABLE IF NOT EXISTS guilds_t (
  id          VARCHAR PRIMARY KEY,
  guild_id    TEXT,
  guild_name  TEXT,
  iconUrl     TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS channels_t (
  id            VARCHAR PRIMARY KEY,
  channel_name  TEXT,
  channel_type  TEXT,
  categoryId    TEXT,
  category      TEXT,
  guild_id      VARCHAR,
  topic         TEXT,
  channel_name_length INT,
  FOREIGN KEY (guild_id) REFERENCES guilds_t(id)
)
""",

"""
CREATE TABLE IF NOT EXISTS messages_dump_t (
  id           VARCHAR PRIMARY KEY,
  guild_id     VARCHAR,
  attachments  TEXT,
  author       TEXT,
  channel_id   VARCHAR,
  content      TEXT,
  interaction  TEXT,
  isBot        BOOLEAN,
  isPinned     BOOLEAN,
  mentions     BOOLEAN,
  msg_type     TEXT,
  timestamp    INT,
  timestampEdited INT,
  content_length INT
)
""",

"""
CREATE TABLE IF NOT EXISTS messages_t (
  id           VARCHAR PRIMARY KEY,
  guild_id     VARCHAR,
  attachments  TEXT,
  author       TEXT,
  channel_id   VARCHAR,
  content      TEXT,
  interaction  TEXT,
  isBot        BOOLEAN,
  isPinned     BOOLEAN,
  mentions     BOOLEAN,
  msg_type     TEXT,
  unix_timestamp    INTEGER,
  unix_timestampEdited INTEGER,
  content_length INT,
  FOREIGN KEY (channel_id) REFERENCES channels_t(id)
)
""",


"""
CREATE TABLE IF NOT EXISTS authors_t (
  id            VARCHAR PRIMARY KEY,
  author_id     VARCHAR,
  name          TEXT,
  nickname      TEXT,
  color         TEXT,
  isBot         BOOLEAN,
  avatarUrl     TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS authors_dump_t (
  id            VARCHAR,
  author_id     VARCHAR,
  name          TEXT,
  nickname      TEXT,
  color         TEXT,
  isBot         BOOLEAN,
  avatarUrl     TEXT
)
""",


"""
CREATE TABLE IF NOT EXISTS attachments_t (
  id                    VARCHAR PRIMARY KEY,
  attachment_url        TEXT,
  attachment_filename   TEXT,
  fileSizeBytes         BIGINT,
  message_id            TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS roles_t (
  id          VARCHAR PRIMARY KEY,
  role_name   TEXT,
  color       TEXT,
  position    BIGINT
)
""",

# """
# ALTER TABLE channels_t
#   ADD CONSTRAINT channels_t_guild_id_to_guilds_t
#   FOREIGN KEY (guild_id)
#   REFERENCES guilds_t(id)
#   ON DELETE CASCADE;
# CREATE INDEX ON channels_t (guild_id);
# """,

# """
# ALTER TABLE messages_t
#   ADD CONSTRAINT message_id_to_channel_id
#   FOREIGN KEY (channel_id)
#   REFERENCES channels_t(id)
#   ON DELETE CASCADE;
# CREATE INDEX ON messages_t (channel_id);
# """,

# """
# ALTER TABLE attachments_t
#   ADD CONSTRAINT attachment_id_to_message_id
#   FOREIGN KEY (message_id)
#   REFERENCES messages_t(id)
#   ON DELETE CASCADE;
# CREATE INDEX ON attachments_t (message_id);
# """
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
      print(query)
      cursor.execute(query)
      conn.commit()
      print("Another table created")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")