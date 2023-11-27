import psycopg2
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()


create_table_queries = [

"""
CREATE TABLE IF NOT EXISTS guilds_t (
  id                VARCHAR PRIMARY KEY,
  guild_name        TEXT,
  icon_url          TEXT,
  un_indexed_json   TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS channels_t (
  id                     VARCHAR PRIMARY KEY,
  channel_name           TEXT,
  channel_type           TEXT,
  category_id            TEXT,
  category               TEXT,
  guild_id               VARCHAR,
  topic                  TEXT,
  channel_name_length    INT,
  un_indexed_json        TEXT,
  FOREIGN KEY (guild_id) REFERENCES guilds_t(id)
)
""",

"""
CREATE TABLE IF NOT EXISTS messages_t (
  id                    VARCHAR PRIMARY KEY,
  guild_id              VARCHAR,
  channel_id            VARCHAR,
  author_id             VARCHAR,
  author_guild_id       VARCHAR,
  msg_content           TEXT,
  msg_content_length    INT,
  -- interaction        TEXT,
  attachments           TEXT,
  is_bot                BOOLEAN,
  is_pinned             BOOLEAN,
  mentions              BOOLEAN,
  msg_type              TEXT,
  msg_timestamp         timestamp,
  msg_timestamp_edited  timestamp,
  reply_to_message_id   VARCHAR,
  un_indexed_json       TEXT,
  FOREIGN KEY (channel_id) REFERENCES channels_t(id)
)
""",

"""
CREATE TABLE IF NOT EXISTS message_urls_t (
  id             VARCHAR PRIMARY KEY,
  message_id     VARCHAR,
  scheme         VARCHAR,
  netloc         VARCHAR,
  path           VARCHAR,
  params         VARCHAR,
  query          VARCHAR,
  fragment       VARCHAR
)
""",

"""
CREATE TABLE IF NOT EXISTS message_replies_t (
  id                       VARCHAR PRIMARY KEY,
  guild_id                 VARCHAR,
  channel_id               VARCHAR,
  author_id                VARCHAR,
  author_guild_id          VARCHAR,
  reply_to_channel_id      VARCHAR,
  reply_to_message_id      VARCHAR,
  reply_to_author_id       VARCHAR,
  reply_to_author_guild_id VARCHAR
)
""",


"""
CREATE TABLE IF NOT EXISTS authors_t (
  id               VARCHAR PRIMARY KEY,
  author_id        VARCHAR,
  guild_id         VARCHAR,
  author_name      TEXT,
  nickname         TEXT,
  color            TEXT,
  is_bot           BOOLEAN,
  avatar_url       TEXT,
  un_indexed_json  TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS reactions_t (
  id                 VARCHAR PRIMARY KEY,
  message_id         VARCHAR,
  author_guild_id    VARCHAR,
  channel_id         VARCHAR,
  guild_id           VARCHAR,
  reaction_count     INTEGER,
  emoji_id           VARCHAR,
  emoji_code         VARCHAR,
  emoji_name         VARCHAR,
  emoji_json         TEXT,
  un_indexed_json    TEXT
)
""",


"""
CREATE TABLE IF NOT EXISTS attachments_t (
  id                    VARCHAR PRIMARY KEY,
  attachment_url        TEXT,
  file_extension        TEXT,
  file_size_bytes       BIGINT,
  message_id            TEXT,
  author_guild_id       VARCHAR,
  guild_id              VARCHAR,
  un_indexed_json TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS roles_t (
  id                  VARCHAR PRIMARY KEY,
  role_id             VARCHAR,
  guild_id            VARCHAR,
  author_guild_id     VARCHAR,
  name                TEXT,
  position            BIGINT,
  un_indexed_json     TEXT
)
""",

"""
CREATE TABLE IF NOT EXISTS mentions_t (
  id                VARCHAR PRIMARY KEY,
  message_id        VARCHAR,
  guild_id          VARCHAR,
  author_guild_id   VARCHAR,
  channel_id        VARCHAR
)
"""
]

constraint_queries = [

"""
ALTER TABLE channels_t
  ADD CONSTRAINT channels_t_guild_id_to_guilds_t
  FOREIGN KEY (guild_id)
  REFERENCES guilds_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON channels_t (guild_id);
""",

"""
ALTER TABLE messages_t
  ADD CONSTRAINT message_id_to_channel_id
  FOREIGN KEY (channel_id)
  REFERENCES channels_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON messages_t (channel_id);
""",

"""
ALTER TABLE messages_t
  ADD CONSTRAINT message_id_to_author_id
  FOREIGN KEY (author_guild_id)
  REFERENCES authors_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON messages_t (channel_id);
""",

"""
ALTER TABLE attachments_t
  ADD CONSTRAINT attachment_id_to_message_id
  FOREIGN KEY (message_id)
  REFERENCES messages_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON attachments_t (message_id);
""",

"""
ALTER TABLE mentions_t
  ADD CONSTRAINT mentions_t_to_messages_t
  FOREIGN KEY (message_id)
  REFERENCES messages_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON mentions_t (message_id);
""",

"""
ALTER TABLE mentions_t
  ADD CONSTRAINT mentions_t_to_guilds_t
  FOREIGN KEY (guild_id)
  REFERENCES guilds_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON mentions_t (guild_id);
""",

"""
ALTER TABLE mentions_t
  ADD CONSTRAINT mentions_t_to_channels_t
  FOREIGN KEY (channel_id)
  REFERENCES channels_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON mentions_t (channel_id);
""",

"""
ALTER TABLE reactions_t
  ADD CONSTRAINT reactions_t_to_messages_t
  FOREIGN KEY (message_id)
  REFERENCES messages_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON reactions_t (message_id);
""",

"""
ALTER TABLE reactions_t
  ADD CONSTRAINT reactions_t_to_channels_t
  FOREIGN KEY (channel_id)
  REFERENCES channels_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON reactions_t (channel_id);
""",

"""
ALTER TABLE reactions_t
  ADD CONSTRAINT reactions_t_to_authors_t
  FOREIGN KEY (author_guild_id)
  REFERENCES authors_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON reactions_t (author_guild_id);
""",

"""
ALTER TABLE roles_t
  ADD CONSTRAINT roles_t_to_guilds_t
  FOREIGN KEY (guild_id)
  REFERENCES guilds_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON roles_t (guild_id);
""",

# Error on this one
"""
ALTER TABLE roles_t
  ADD CONSTRAINT roles_t_to_authors_t
  FOREIGN KEY (author_guild_id)
  REFERENCES authors_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON roles_t (author_guild_id);
""",

"""
ALTER TABLE message_replies_t
  ADD CONSTRAINT message_replies_t_to_channels_t
  FOREIGN KEY (channel_id)
  REFERENCES channels_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON message_replies_t (channel_id);
""",

"""
ALTER TABLE message_replies_t
  ADD CONSTRAINT message_replies_t_to_authors_t
  FOREIGN KEY (author_guild_id)
  REFERENCES authors_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON message_replies_t (author_guild_id);
""",

"""
ALTER TABLE message_replies_t
  ADD CONSTRAINT message_replies_t_to_authors_t_for_reply
  FOREIGN KEY (reply_to_author_guild_id)
  REFERENCES authors_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON message_replies_t (reply_to_author_guild_id);
""",

# This Query Fails
"""
ALTER TABLE message_replies_t
  ADD CONSTRAINT message_replies_t_to_channels_t_for_reply
  FOREIGN KEY (reply_to_channel_id)
  REFERENCES channels_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON message_replies_t (reply_to_channel_id);
"""
]

# try:
#     url = urlparse(os.environ.get("postgres_url"))
#     print(url)
    # conn = psycopg2.connect(
    #     host=url.hostname,
    #     port=url.port,
    #     database=url.path[1:],
    #     user=url.username,
    #     password=url.password
    # )
    # cursor = conn.cursor()
#     for query in create_table_queries:
#       print(query)
#       cursor.execute(query)
#       conn.commit()
#       print("Another table created")
#     cursor.close()
#     conn.close()

# except Exception as e:
#     print(f"Error: {e}")