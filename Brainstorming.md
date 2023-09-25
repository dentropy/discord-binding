

## DROP TABLES

``` sql
DROP TABLE messages;
DROP TABLE guilds;
DROP TABLE channels;
DROP TABLE embeds;
DROP TABLE embeds;
DROP TABLE embeds;
```


## Get my messages in the order I sent them

``` sql

SELECT DISTINCT content, timestamp
FROM messages
INNER JOIN authors ON messages.author = authors.id
WHERE authors.name = 'dentropy'
ORDER BY timestamp ASC;


```

## Get the longest messages and the person who sent them

``` sql

SELECT DISTINCT content, authors.name
FROM messages
INNER JOIN authors ON messages.author = authors.id
ORDER BY LENGTH(content) DESC;

```

## Get my messages ordered by length

``` sql

SELECT DISTINCT content, timestamp
FROM messages
INNER JOIN authors ON messages.author = authors.id
WHERE authors.name = 'dentropy'
ORDER BY LENGTH(content) DESC;

```

## Most Reactions


``` sql

SELECT count, content, name
FROM reactions
INNER JOIN messages ON messages.id = reactions.message_id
INNER JOIN authors ON messages.author = authors.id
GROUP BY message_id
order by count desc;

```

## Total Number of Messages

``` sql

SELECT COUNT(*) FROM messages;

```

## Get all the json key's from a raw_json column

``` sql

SELECT DISTINCT json_tree.key as keyname
FROM raw_messages_t
JOIN json_tree(raw_messages_t.raw_json) ON 1
ORDER BY keyname ASC;

SELECT
    json_extract(raw_json, '$.interaction') as interaction
FROM raw_messages_t
WHERE interaction IS NOT NULL;
```

``` sql

CREATE TABLE messages_t (
  id INT PRIMARY KEY,
  attachments BOOLEAN,
  author INT,
  channel_id INT,
  content TEXT,
  interaction JSON,
  isBot BOOLEAN,
  isPinned BOOLEAN,
  mentions BOOLEAN,
  msg_type VARCHAR
)

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
  raw_messages_t
LIMIT 5;

```

``` sql

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

CREATE TABLE IF NOT EXISTS guilds_t AS
SELECT
  json_extract(raw_json, '$.id') as guild_id,
  json_extract(raw_json, '$.name') as guild_name,
  json_extract(raw_json, '$.iconUrl') as iconUrl
FROM raw_guilds_t;

CREATE TABLE IF NOT EXISTS roles_t AS
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as role_id,
  json_extract(raw_json, '$.role_name') as role_name,
  json_extract(raw_json, '$.color') as color,
  json_extract(raw_json, '$.position') as position
FROM raw_roles_t;

CREATE TABLE IF NOT EXISTS attachments_t AS
SELECT
  DISTINCT(json_extract(raw_json, '$.id')) as attachment_id,
  json_extract(raw_json, '$.attachment_url') as attachment_url,
  json_extract(raw_json, '$.fileName') as attachment_filename,
  json_extract(raw_json, '$.fileSizeBytes') as fileSizeBytes,
  json_extract(raw_json, '$.message_id') as message_id
FROM raw_attachments_t;

```