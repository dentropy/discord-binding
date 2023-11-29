import requests

api_url = "http://localhost:8000/"

print("Testing list_guilds")
form_data = {
    "query_name" : "list_guilds"
}
response = requests.post(api_url + "/query/", data=form_data)
result = response.json()[0]
#print(result)
assert len(result.keys()) == 2


guild_id = result["guild_id"]


print("Testing guild_channels")
form_data = {
    "query_name" : "guild_channels",
    "guild_id"   : guild_id
}
response = requests.post(api_url + "/query/", data=form_data)
result = response.json()[0]
# print(result)
assert len(result.keys()) == 4


channel_id = result["channel_id"]



print("Testing channel_authors")
form_data = {
    "query_name"   : "channel_authors",
    "channel_id"   : channel_id
}
response = requests.post(api_url + "/query/", data=form_data)
result = response.json()[0]
# print(result)
assert len(result.keys()) == 4



print("Testing channel_messages")
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

