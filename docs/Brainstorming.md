
## Test Script

``` python
import os
from dotenv import load_dotenv
load_dotenv()
from DiscordAnalytics import DiscordAnalytics
discord_analytics = DiscordAnalytics(os.environ.get("db_url"))

guilds_list = discord_analytics.fetch_all_guilds()
discord_analytics.set_guild_white_list(list(guilds_list["guild_id"]))
discord_analytics.calculate_base_guild_stats()
discord_analytics.calulate_demo_guild_stats()
discord_analytics.caultate_monthly_guild_stats()
contact_df = discord_analytics.concat_month_df_with_base_df()
```

## Add Constraints Queries

``` SQL
ALTER TABLE messages_t
ADD COLUMN real_timestamp timestamp WITHOUT TIME ZONE;

ALTER TABLE messages_t
ADD COLUMN real_timestamp_edited timestamp WITHOUT TIME ZONE;

UPDATE messages_t
SET real_timestamp = to_timestamp(unix_timestamp);

ALTER TABLE messages_t
  ADD CONSTRAINT messages_t_to_guild_id
  FOREIGN KEY (guild_id)
  REFERENCES guilds_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON messages_t (guild_id);
```

## DON'T RUN THIS

``` SQL
ALTER TABLE messages_dump_t
DROP COLUMN #real_timestamp;
```


## Testing Queries

``` sql
select * from guilds_t;
select * from channels_t;
select * from messages_t;
select count(*) from messages_t;
select * from authors_t;
select * from reactions_t;
select * from attachments_t;
select * from roles_t;
select count(*) from roles_t;
select count(*) from messages_t;
select * from mentions_t;
select count(*) from mentions_t;
```

## DROP TABLES

``` sql

drop table if exists "attachments_t" cascade;
drop table if exists "guilds_t" cascade;
drop table if exists "channels_t" cascade;
drop table if exists "messages_dump_t" cascade;
drop table if exists "messages_t" cascade;
drop table if exists "authors_t" cascade;
drop table if exists "authors_dump_t" cascade;
drop table if exists "roles_t" cascade;
drop table if exists "reactions_t" cascade;
if exists "mentions_t" cascade;

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

## Helpers

You can check if the SQLite database is being written to with `ls -lrt` a couple times in the directory of the database to see if it is increasing.

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

## Prisma Setup

``` bash
cp ./out/GUILD.sqlite dev.db
python3 fix_schema.py dev.db
sqlitebrowser dev.db # optional
cp dev.db GraphQL/prisma
cd GraphQL
npx prisma db pull
npx prisma generate
```

## Postgres Fix Schema

``` SQL
ALTER TABLE channels_t
  ADD CONSTRAINT channels_t_guild_id_to_guilds_t
  FOREIGN KEY (guild_id)
  REFERENCES guilds_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON channels_t (guild_id);


ALTER TABLE messages_t
  ADD CONSTRAINT message_id_to_channel_id
  FOREIGN KEY (channel_id)
  REFERENCES channels_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON messages_t (channel_id);


ALTER TABLE attachments_t
  ADD CONSTRAINT attachment_id_to_message_id
  FOREIGN KEY (message_id)
  REFERENCES messages_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON attachments_t (message_id);

```

## Migrate tables, we don't do this anymore

``` sql
INSERT INTO messages_t
            (
                        id,
                        channnel_id,
                        attachments,
                        author,
                        content,
                        interaction,
                        ispinned,
                        mentions,
                        msg_type,
                        timestamp,
                        timestampedited,
                        content_length
            )
            (
                   SELECT id,
                          channel_id,
                          attachments,
                          author,
                          content,
                          interaction,
                          ispinned,
                          mentions,
                          msg_type,
                          To_timestamp(timestamp),
                          To_timestamp(timestampedited),
                          content_length
                   FROM   messages_dump_t )
on conflict
            (
                        id
            )
            do nothing;
```
``` sql
INSERT INTO messages_t (
    id,
    channel_id,
    attachments,
    author,
    content,
    interaction,
    ispinned,
    mentions,
    msg_type,
    timestamp,
    timestampedited,
    content_length
) 
SELECT 
    id,
    channel_id,
    attachments,
    author,
    content,
    interaction,
    ispinned,
    mentions,
    msg_type,
    TO_TIMESTAMP(timestamp),
    TO_TIMESTAMP(timestampedited),
    content_length
FROM messages_dump_t
WHERE channel_id  IN (
    SELECT id
    FROM channels_t 
)
ON CONFLICT (id) DO NOTHING;
```


``` sql
ALTER TABLE messages_t
  ADD CONSTRAINT message_id_to_author_id
  FOREIGN KEY (author)
  REFERENCES authors_t(author_id)
  ON DELETE CASCADE;
CREATE INDEX ON messages_t(author);
```