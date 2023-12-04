from urllib.parse import urlparse
from pprint import pprint
import pandas as pd
from pprint import pprint

from modules.query_resolver import query_resolver

import psycopg2
import psycopg2.extras

import os
from decouple import AutoConfig
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
config = AutoConfig(search_path=current_directory)
url = urlparse(config("db_url"))
connection = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)
cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


from tests.postgresql_query_test import test_queries
from modules.query_resolver import query_resolver
from modules.queries import queries


result = query_resolver(cursor, queries, "list_guilds")
guild_id = result.iloc[0]["guild_id"]
# print("list_guilds")
print(f"guild_id = {guild_id}")
# pprint(result)
assert result.shape[1] == 3

result = query_resolver(cursor, queries, "guild_channels", {
    "guild_id" : guild_id
})
channel_id = result.iloc[0]["channel_id"]
# print("guild_channels")
print(f"channel_id = {channel_id}")
# pprint(result)
assert result.shape[1] == 5

result = query_resolver(cursor, queries, "guild_authors", {
    "guild_id" : guild_id
})
# print("guild_authors")
# pprint(result)
assert result.shape[1] == 5

result = query_resolver(cursor, queries, "channel_authors", {
    "channel_id" : channel_id
})
# print("channel_authors")
# pprint(result)
assert result.shape[1] == 4


query_name = "channel_messages"
result = query_resolver(cursor, queries, query_name, {
    "channel_id" : channel_id,
    "order"      : "desc",
    "offset"     : 1
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 10

query_name = "user_longest_avg_msg_length"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 5


query_name = "guild_author_most_messages"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 6


query_name = "guild_author_most_days_with_messages"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 6



query_name = "guild_author_most_reactions"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 6

query_name = "guild_author_distinct_reaction_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 6


query_name = "guild_author_most_messages_single_day"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
author_id = result.iloc[0]["author_guild_id"]
print(f"author_id = {author_id}")
assert result.shape[1] == 6


query_name = "guild_author_most_attachments"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id,
    "author_id" : author_id
})
# print(query_name)
# pprint(result)
attachment_author_id = result.iloc[0]["author_guild_id"]
print(f"attachment_author_id = {attachment_author_id}")
assert result.shape[1] == 6


query_name = "guild_author_edit_percentage"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 8


query_name = "guild_author_most_question_messages"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
assert result.shape[1] == 5


query_name = "count_messages_per_channel_for_user_in_guild"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id,
    "author_id" : author_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 8


query_name = "guild_author_most_reacted_messages"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id,
    "author_id" : author_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 8


query_name = "guild_author_messages_by_hour_of_day"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id,
    "author_id" : author_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 7

query_name = "guild_author_most_reaction_to_attachment"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id,
    "author_id" : attachment_author_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 8

query_name = "guild_author_messages_day_of_week"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id,
    "author_id" : attachment_author_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[0] == 7
assert result.shape[1] == 8


query_name = "guild_author_most_messages"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 6


query_name = "guild_activity_per_month"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 4


query_name = "guild_channels_most_active"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 5


query_name = "guild_messages_percent_total_days"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[0] == 1
assert result.shape[1] == 7



query_name = "guild_bots_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[0] == 1
assert result.shape[1] == 1


query_name = "guild_author_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[0] == 1
assert result.shape[1] == 1


query_name = "guild_channels_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[0] == 1
assert result.shape[1] == 1


query_name = "guild_oldest_message"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[0] == 1
assert result.shape[1] == 9


query_name = "guild_message_per_channel"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 7


query_name = "guild_attachment_file_type_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 4



query_name = "guild_attachment_reactions"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 8


query_name = "guild_messages_month"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 4


query_name = "guild_channel_author_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 4

query_name = "guild_author_mention_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 6


query_name = "guild_domain_count"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 2


query_name = "guild_author_url_react"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 9


query_name = "guild_author_message_min_100"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 7


query_name = "guild_channel_message_length"
result = query_resolver(cursor, queries, query_name, {
    "guild_id"  : guild_id
})
# print(query_name)
# pprint(result)
# print(result.shape[1])
assert result.shape[1] == 5



print("TEST SUCCESS")