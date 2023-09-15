import sqlite3

queries = ["""
CREATE TABLE IF NOT EXISTS messages_t AS
SELECT
  json_extract(raw_json, '$.id') as id,
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
  json_extract(raw_json, '$.id') as id,
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

print("Don't forget to update path to database in this file, I will add CLI arguments for this later")
sqlite3_connection = sqlite3.connect("./test.db")
sqlite3_cursor = sqlite3_connection.cursor()
for query in queries:
  sqlite3_cursor.execute(query)
sqlite3_connection.commit()