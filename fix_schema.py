import sqlite3
import sys
if len(sys.argv) != 2:
    print("Usage: python fix_schema.py <argument>")
    sys.exit(1)

queries = ["""
CREATE TABLE IF NOT EXISTS messages_t AS
SELECT
  json_extract(raw_json, '$.id') as message_id,
  json_extract(raw_json, '$.attachments') as attachments,
  json_extract(raw_json, '$.author') as author,
  json_extract(raw_json, '$.channel_id') as channel_id,
  json_extract(raw_json, '$.content') as content,
  json_extract(raw_json, '$.interaction') as interaction,
  json_extract(raw_json, '$.isBot') as isBot,
  json_extract(raw_json, '$.isPinned') as isPinned,
  json_extract(raw_json, '$.mentions') as mentions,
  json_extract(raw_json, '$.type') as msg_type
FROM
  raw_messages_t;
""",

"""
CREATE TABLE IF NOT EXISTS channels_t AS
SELECT
  json_extract(raw_json, '$.id') as channel_id,
  json_extract(raw_json, '$.name') as channel_name,
  json_extract(raw_json, '$.type') as channel_type,
  json_extract(raw_json, '$.categoryId') as categoryId,
  json_extract(raw_json, '$.category') as category,
  json_extract(raw_json, '$.guild_id') as guild_id,
  json_extract(raw_json, '$.topic') as topic
FROM
  raw_channels_t;
""",

"""
CREATE TABLE IF NOT EXISTS guilds_t AS
SELECT
  json_extract(raw_json, '$.id') as guild_id,
  json_extract(raw_json, '$.name') as guild_name,
  json_extract(raw_json, '$.iconUrl') as iconUrl
FROM raw_guilds_t;
""",

"""
CREATE TABLE IF NOT EXISTS roles_t AS
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as role_id,
  json_extract(raw_json, '$.role_name') as role_name,
  json_extract(raw_json, '$.color') as color,
  json_extract(raw_json, '$.position') as position
FROM raw_roles_t;
""",

"""
CREATE TABLE IF NOT EXISTS attachments_t AS
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as attachment_id,
  json_extract(raw_json, '$.attachment_url') as attachment_url,
  json_extract(raw_json, '$.fileName') as attachment_filename,
  json_extract(raw_json, '$.fileSizeBytes') as fileSizeBytes,
  json_extract(raw_json, '$.message_id') as message_id
FROM raw_attachments_t;
"""]

table_type_queries = [

"""
DROP TABLE IF EXISTS guilds_t;
""",

"""
DROP TABLE IF EXISTS channels_t;
""",

"""
DROP TABLE IF EXISTS messages_t;
""",

"""
DROP TABLE IF EXISTS authors_t;
""",

"""
DROP TABLE IF EXISTS attachments_t;
""",

"""
DROP TABLE IF EXISTS roles_t;
""",

"""
CREATE TABLE IF NOT EXISTS guilds_t (
  id          INTEGER PRIMARY KEY,
  guild_id    TEXT,
  guild_name  TEXT,
  iconUrl     TEXT
)
""",

"""
INSERT INTO guilds_t (id, guild_name, iconUrl)
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as id,
  json_extract(raw_json, '$.name') as guild_name,
  json_extract(raw_json, '$.iconUrl') as iconUrl
FROM raw_guilds_t
LIMIT 1;
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
INSERT INTO channels_t (id, channel_name, channel_type, categoryId, category, guild_id, topic, channel_name_length)
SELECT
  DISTINCT( json_extract(raw_json, '$.id')) as id,
  json_extract(raw_json, '$.name') as channel_name,
  json_extract(raw_json, '$.type') as channel_type,
  json_extract(raw_json, '$.categoryId') as categoryId,
  json_extract(raw_json, '$.category') as category,
  json_extract(raw_json, '$.guild_id') as guild_id,
  json_extract(raw_json, '$.topic') as topic,
  LENGTH(json_extract(raw_json, '$.name')) as channel_name_length
FROM
  raw_channels_t;
""",

"""
CREATE TABLE IF NOT EXISTS messages_t (
  id           INTEGER PRIMARY KEY,
  guild_id     TEXT,
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
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id     INTEGER,
  name          TEXT,
  nickname      TEXT,
  color         TEXT,
  isBot         BOOLEAN,
  avatarUrl     TEXT
)
""",


"""
INSERT INTO authors_t (author_id, name, nickname, color, isBot, avatarUrl)
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as author_id,
  json_extract(raw_json, '$.name') as name,
  json_extract(raw_json, '$.nickname') as nickname,
  json_extract(raw_json, '$.color') as color,
  json_extract(raw_json, '$.isBot') as isBot,
  json_extract(raw_json, '$.avatarUrl') as avatarUrl
FROM raw_authors_t;
""",


"""
INSERT INTO messages_t (id, guild_id, attachments, author, channel_id, content, interaction, isBot, isPinned, mentions, msg_type, timestamp, timestampEdited, content_length)
SELECT
  json_extract(raw_json, '$.id') as id,
  json_extract(raw_json, '$.guild_id') as guild_id,
  json_extract(raw_json, '$.attachments') as attachments,
  json_extract(raw_json, '$.author') as author,
  json_extract(raw_json, '$.channel_id') as channel_id,
  json_extract(raw_json, '$.content') as content,
  json_extract(raw_json, '$.interaction') as interaction,
  json_extract(raw_json, '$.isBot') as isBot,
  json_extract(raw_json, '$.isPinned') as isPinned,
  json_extract(raw_json, '$.mentions') as mentions,
  json_extract(raw_json, '$.type') as msg_type,
  strftime('%s', json_extract(raw_json, '$.timestamp')) as timestamp,
  strftime('%s', json_extract(raw_json, '$.timestampEdited')) as timestampEdited,
  LENGTH(json_extract(raw_json, '$.content')) as content_length
FROM
  raw_messages_t;
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
INSERT INTO attachments_t (id, attachment_url, attachment_filename, fileSizeBytes, message_id)
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as id,
  json_extract(raw_json, '$.attachment_url') as attachment_url,
  json_extract(raw_json, '$.fileName') as attachment_filename,
  json_extract(raw_json, '$.fileSizeBytes') as fileSizeBytes,
  json_extract(raw_json, '$.message_id') as message_id
FROM raw_attachments_t;
""",

"""
CREATE TABLE IF NOT EXISTS roles_t (
  id          INTEGER PRIMARY KEY,
  role_name   TEXT,
  color       TEXT,
  position    INTEGER
)
""",

"""
INSERT INTO roles_t (id, role_name, color, position)
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as id,
  json_extract(raw_json, '$.role_name') as role_name,
  json_extract(raw_json, '$.color') as color,
  json_extract(raw_json, '$.position') as position
FROM raw_roles_t;
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
  file_size_bytes       BIGINT,

)
""",

]


sqlite3_connection = sqlite3.connect(sys.argv[1])
sqlite3_cursor = sqlite3_connection.cursor()
for query in table_type_queries:
  print(query)
  print("\n\n")
  sqlite3_cursor.execute(query)
  sqlite3_connection.commit()
