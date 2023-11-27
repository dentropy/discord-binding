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


result = query_resolver(cursor, queries, "channel_messages", {
    "channel_id" : channel_id,
    "order"      : "desc",
    "offset"     : 1
})
# print("channel_messages")
# pprint(result)
assert result.shape[1] == 6


