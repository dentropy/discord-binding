import requests
from pprint import pprint

api_url = "http://localhost:8000/"

print("\n\nTesting /query API Endpoint")
print("/query list_guilds")
form_data = {
    "query_name" : "list_guilds"
}
response = requests.post(api_url + "/query/", data=form_data)
result = response.json()[0]
# print(result)
assert len(result.keys()) == 3


guild_id = result["guild_id"]


print("/query guild_channels")
form_data = {
    "query_name" : "guild_channels",
    "guild_id"   : guild_id
}
response = requests.post(api_url + "/query/", data=form_data)
result = response.json()[0]
# print(result)
# print(len(result.keys()))
assert len(result.keys()) == 5


channel_id = result["channel_id"]



print("/query channel_authors")
form_data = {
    "query_name"   : "channel_authors",
    "channel_id"   : channel_id
}
response = requests.post(api_url + "/query/", data=form_data)
result = response.json()[0]
# print(result)
assert len(result.keys()) == 4



print("/query channel_messages")
form_data = {
    "query_name"   : "channel_messages",
    "channel_id"   : channel_id,
    "order"        : "desc",
    "offset"       : 0
}
response = requests.post(api_url + "/query/", data=form_data)
result = response.json()[0]
# print(result)
assert len(result.keys()) == 10

print("\n\nTesting /list_graphs API Endpoint")
response = requests.get(api_url + "/list_graphs/")
result = response.json()
# pprint(result)
# pprint(len(result))
assert len(result) == 13
print("/list_queries endpoint works")



print("\n\nTesting plotly_graph API Endpoint")

graph_name = "user_longest_avg_msg_length"
print("/plotly_graph user_longest_avg_msg_length")
# print(f"\n\nTesting {graph_name}\n\n")
form_data = {
    "graph_name"   : graph_name,
    "guild_id"     : guild_id
}
# print(guild_id)
# pprint(form_data)
response = requests.post(api_url + "/plotly_graph/", data=form_data)
result = response.json()
# pprint(result)


print("\n\nTEST SUCCESS")