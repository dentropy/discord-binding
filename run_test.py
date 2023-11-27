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
assert result.shape[1] == 2

result = query_resolver(cursor, queries, "guild_channels", {
    "guild_id" : guild_id
})
channel_id = result.iloc[0]["channel_id"]
# print("guild_channels")
print(f"channel_id = {channel_id}")
# pprint(result)
assert result.shape[1] == 4

result = query_resolver(cursor, queries, "guild_authors", {
    "guild_id" : guild_id
})
# print("guild_authors")
# pprint(result)
assert result.shape[1] == 4

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


result = query_resolver(cursor, queries, "user_longest_avg_msg_length", {
    "guild_id" : guild_id
})
# print("user_longest_avg_msg_length")
# pprint(result)
assert result.shape[1] == 5

result = query_resolver(cursor, queries, "user_longest_avg_msg_length", {
    "guild_id" : guild_id
})
# print("user_longest_avg_msg_length")
# pprint(result)
assert result.shape[1] == 5


result = query_resolver(cursor, queries, "guild_author_most_messages", {
    "guild_id" : guild_id
})
# print("guild_author_most_messages")
# pprint(result)
assert result.shape[1] == 6

result = query_resolver(cursor, queries, "guild_author_consistent", {
    "guild_id" : guild_id
})
# print("guild_author_most_messages")
# pprint(result)
assert result.shape[1] == 6


result = query_resolver(cursor, queries, "guild_author_most_reactions", {
    "guild_id" : guild_id
})
# print("guild_author_most_messages")
# pprint(result)
assert result.shape[1] == 6


result = query_resolver(cursor, queries, "guild_author_distinct_reaction_count", {
    "guild_id" : guild_id
})
# print("guild_author_most_messages")
# pprint(result)
assert result.shape[1] == 6


query_name = "guild_author_most_messages_single_day"
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
assert result.shape[1] == 6


query_name = "guild_author_most_attachments"
result = query_resolver(cursor, queries, query_name, {
    "guild_id" : guild_id
})
# print(query_name)
# pprint(result)
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

print("TEST SUCCESS")