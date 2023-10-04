import sqlite3
import sys
if len(sys.argv) != 2:
    print("Usage: python fix_schema.py <argument>")
    sys.exit(1)

queries = ["""
CREATE TABLE IF NOT EXISTS messages_t AS
SELECT
  json_extract_path_text(raw_json::json, 'id') as message_id,
  json_extract_path_text(raw_json::json, 'attachments') as attachments,
  json_extract_path_text(raw_json::json, 'author') as author,
  json_extract_path_text(raw_json::json, 'channel_id') as channel_id,
  json_extract_path_text(raw_json::json, 'content') as content,
  json_extract_path_text(raw_json::json, 'interaction') as interaction,
  json_extract_path_text(raw_json::json, 'isBot') as isBot,
  json_extract_path_text(raw_json::json, 'isPinned') as isPinned,
  json_extract_path_text(raw_json::json, 'mentions') as mentions,
  json_extract_path_text(raw_json::json, 'type') as msg_type
FROM
  raw_messages_t;
""",

"""
CREATE TABLE IF NOT EXISTS channels_t AS
SELECT
  json_extract_path_text(raw_json::json, 'id') as channel_id,
  json_extract_path_text(raw_json::json, 'name') as channel_name,
  json_extract_path_text(raw_json::json, 'type') as channel_type,
  json_extract_path_text(raw_json::json, 'categoryId') as categoryId,
  json_extract_path_text(raw_json::json, 'category') as category,
  json_extract_path_text(raw_json::json, 'guild_id') as guild_id,
  json_extract_path_text(raw_json::json, 'topic') as topic
FROM
  raw_channels_t;
""",

"""
CREATE TABLE IF NOT EXISTS guilds_t AS
SELECT
  json_extract_path_text(raw_json::json, 'id') as guild_id,
  json_extract_path_text(raw_json::json, 'name') as guild_name,
  json_extract_path_text(raw_json::json, 'iconUrl') as iconUrl
FROM raw_guilds_t;
""",

"""
CREATE TABLE IF NOT EXISTS roles_t AS
SELECT
  DISTINCT(json_extract_path_text(raw_json::json, 'id')) as role_id,
  json_extract_path_text(raw_json::json, 'role_name') as role_name,
  json_extract_path_text(raw_json::json, 'color') as color,
  json_extract_path_text(raw_json::json, 'position') as position
FROM raw_roles_t;
""",

"""
CREATE TABLE IF NOT EXISTS attachments_t AS
SELECT
  DISTINCT(json_extract_path_text(raw_json::json, 'id')) as attachment_id,
  json_extract_path_text(raw_json::json, 'attachment_url') as attachment_url,
  json_extract_path_text(raw_json::json, 'fileName') as attachment_filename,
  CAST( json_extract_path_text(raw_json::json, 'fileSizeBytes') as BIGINT) as fileSizeBytes,
  json_extract_path_text(raw_json::json, 'message_id') as message_id
FROM raw_attachments_t;
"""]

table_type_queries = [

# """
# DROP TABLE IF EXISTS attachments_t;
# """,

# """
# DROP TABLE IF EXISTS messages_t;
# """,

# """
# DROP TABLE IF EXISTS authors_t;
# """,

# """
# DROP TABLE IF EXISTS roles_t;
# """,

# """
# DROP TABLE IF EXISTS channels_t;
# """,

# """
# DROP TABLE IF EXISTS guilds_t;
# """,

"""
CREATE TABLE IF NOT EXISTS guilds_t (
  id          VARCHAR PRIMARY KEY,
  guild_name  TEXT,
  iconUrl     TEXT
)
""",

"""
INSERT INTO guilds_t (id, guild_name, iconUrl)
SELECT
  DISTINCT(json_extract_path_text(raw_json::json, 'id')) as id,
  json_extract_path_text(raw_json::json, 'name') as guild_name,
  json_extract_path_text(raw_json::json, 'iconUrl') as iconUrl
FROM raw_guilds_t
on conflict on constraint guilds_t_pkey do nothing;
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
INSERT INTO channels_t (id, channel_name, channel_type, categoryId, category, guild_id, topic, channel_name_length)
SELECT
  DISTINCT( json_extract_path_text(raw_json::json, 'id')) as id,
  json_extract_path_text(raw_json::json, 'name') as channel_name,
  json_extract_path_text(raw_json::json, 'type') as channel_type,
  json_extract_path_text(raw_json::json, 'categoryId') as categoryId,
  json_extract_path_text(raw_json::json, 'category') as category,
  json_extract_path_text(raw_json::json, 'guild_id') as guild_id,
  json_extract_path_text(raw_json::json, 'topic') as topic,
  LENGTH(json_extract_path_text(raw_json::json, 'name')) as channel_name_length
FROM
  raw_channels_t
on conflict (id) do nothing;
""",

"""
CREATE TABLE IF NOT EXISTS messages_t (
  id           VARCHAR PRIMARY KEY,
  guild_id     TEXT,
  attachments  TEXT,
  author       TEXT,
  channel_id   VARCHAR,
  content      TEXT,
  interaction  TEXT,
  isBot        BOOLEAN,
  isPinned     BOOLEAN,
  mentions     BOOLEAN,
  msg_type     TEXT,
  msg_timestamp    timestamp,
  msg_timestampEdited timestamp NULL,
  content_length INT,
  FOREIGN KEY (channel_id) REFERENCES channels_t(id)
)
""",


"""
CREATE TABLE IF NOT EXISTS authors_t (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id     VARCHAR,
  guild_id      VARCHAR,
  name          TEXT,
  nickname      TEXT,
  color         TEXT,
  isBot         BOOLEAN,
  avatarUrl     TEXT
)
""",


"""
INSERT INTO authors_t (author_id, guild_id, name, nickname, color, isBot, avatarUrl)
SELECT
  DISTINCT(cast (  json_extract_path_text(raw_json::json, 'id') as VARCHAR  )) as author_id,
  (cast (  json_extract_path_text(raw_json::json, 'guild_id') as VARCHAR  )) as author_guild_id,
  json_extract_path_text(raw_json::json, 'name') as name,
  json_extract_path_text(raw_json::json, 'nickname') as nickname,
  json_extract_path_text(raw_json::json, 'color') as color,
  cast(json_extract_path_text(raw_json::json, 'isBot') as BOOLEAN) as isBot,
  json_extract_path_text(raw_json::json, 'avatarUrl') as avatarUrl
FROM raw_authors_t;

# """,


"""
INSERT INTO messages_t (id, guild_id, attachments, author, channel_id, content, interaction, isBot, isPinned, mentions, msg_type, msg_timestamp, msg_timestampEdited, content_length)
SELECT
  json_extract_path_text(raw_json::json, 'id') as id,
  json_extract_path_text(raw_json::json, 'guild_id') as guild_id,
  json_extract_path_text(raw_json::json, 'attachments') as attachments,
  json_extract_path_text(raw_json::json, 'author') as author,
  json_extract_path_text(raw_json::json, 'channel_id') as channel_id,
  json_extract_path_text(raw_json::json, 'content') as content,
  json_extract_path_text(raw_json::json, 'interaction') as interaction,
  CAST( json_extract_path_text(raw_json::json, 'isBot') as BOOLEAN ) as isBot,
  CAST( json_extract_path_text(raw_json::json, 'isPinned')  as BOOLEAN) as isPinned,
  CAST( json_extract_path_text(raw_json::json, 'mentions') as BOOLEAN) as mentions,
  json_extract_path_text(raw_json::json, 'type') as msg_type,
  to_timestamp( json_extract_path_text(raw_json::json, 'timestamp'), 'YYYY-MM-DDTHH24:MI:SS' ) as timestamp,
  to_timestamp( json_extract_path_text(raw_json::json, 'timestampEdited'), 'YYYY-MM-DDTHH24:MI:SS' ) as timestampEdited,
  LENGTH(json_extract_path_text(raw_json::json, 'content')) as content_length
FROM
  raw_messages_t;
""",

"""
CREATE TABLE IF NOT EXISTS attachments_t (
  id                    INTEGER PRIMARY KEY,
  attachment_url        TEXT,
  attachment_filename   TEXT,
  fileSizeBytes         BIGINT,
  message_id            INTEGER
)
""",

"""
INSERT INTO attachments_t (id, attachment_url, attachment_filename, fileSizeBytes, message_id)
SELECT
  DISTINCT(json_extract_path_text(raw_json::json, 'id')) as id,
  json_extract_path_text(raw_json::json, 'attachment_url') as attachment_url,
  json_extract_path_text(raw_json::json, 'fileName') as attachment_filename,
  CAST( json_extract_path_text(raw_json::json, 'fileSizeBytes')  as BIGINT)as fileSizeBytes,
  json_extract_path_text(raw_json::json, 'message_id') as message_id
FROM raw_attachments_t
ON CONFLICT (id) DO NOTHING;
""",

"""
CREATE TABLE IF NOT EXISTS roles_t (
  id          VARCHAR PRIMARY KEY,
  role_name   TEXT,
  color       TEXT,
  position    INTEGER
)
""",

"""
INSERT INTO roles_t (id, role_name, color, position)
SELECT
  DISTINCT(CAST(  json_extract_path_text(raw_json::json, 'id')  as VARCHAR) ) as id,
  json_extract_path_text(raw_json::json, 'role_name') as role_name,
  json_extract_path_text(raw_json::json, 'color') as color,
  CAST(  json_extract_path_text(raw_json::json, 'position') AS INTEGER) as position
FROM raw_roles_t
ON CONFLICT (id) DO NOTHING;
""",

"""
CREATE TABLE IF NOT EXISTS roles_metadata_t (
  author_guild_id   TEXT PRIMARY KEY,
  guild_id          TEXT,
  author_id         TEXT,
  role_id           TEXT
)
""",



"""
CREATE TABLE IF NOT EXISTS attachments_metadata_t (
  attachment_id         TEXT PRIMARY KEY,
  message_id            TEXT,
  message_id            TEXT,
  author_id             TEXT,
  author_guild_id       TEXT,
  guild_id              TEXT,
  attachment_url        TEXT,
  attachment_filename   TEXT,
  attachment_file_type  TEXT,
  file_size_bytes       BIGINT
)
""",

]

from urllib.parse import urlparse
import psycopg2
url = urlparse(sys.argv[1])
print(url)
connection = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)
cursor = connection.cursor()
for query in table_type_queries:
  print(query)
  print("\n\n")
  cursor.execute(query)
  connection.commit()
