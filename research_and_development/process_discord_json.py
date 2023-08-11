from pprint import pprint
import os
import glob
import json


def process_discord_json(base_directory):
    json_files = glob.glob(os.path.join(base_directory, '*.json'), recursive=True)
    root_dict = {}
    root_dict["guilds"] = []
    root_dict["channels"] = []
    root_dict["messages"] = []
    # Parts of a message
    root_dict["authors"] = {}
    root_dict["roles"] = []
    root_dict["attachments"] = []
    root_dict["embeds"] = []
    root_dict["stickers"] = []
    root_dict["reactions"] = []
    root_dict["mentions"] = []
    for json_file_path in json_files:
        with open(json_file_path, 'r') as json_file:
            try:
                # print(f"Processing {json_file}")
                data = json.load(json_file)
            except Exception as e:
                continue
        root_dict["guilds"].append(data["guild"])
        data["channel"]["guild_id"] = data["guild"]["id"]
        root_dict["channels"].append(data["channel"])
        for message in data["messages"]:
            if "roles" in message["author"].keys():
                if message["author"]["roles"] != []:
                    for role in message["author"]["roles"]:
                        role["user_id"] = message["author"]
                        root_dict["roles"].append(role)
                del message["author"]["roles"]   
            root_dict["authors"][message["author"]["id"]] = message["author"]
            message["author"] = message["author"]["id"]
            if message["attachments"] != []:
                for attachment in message["attachments"]:
                    attachment["message_id"] = message["id"]
                    root_dict["attachments"].append(attachment)
                message["attachments"] = True
            else:
                message["attachments"] = False
            if message["embeds"] != []:
                for embed in message["embeds"]:
                    embed["message_id"] = message["id"]
                    if "image" not in embed.keys():
                        embed["image"] = ""
                    if "footer" not in embed.keys():
                        embed["footer"] = ""
                    root_dict["embeds"].append(embed)
                message["embeds"] = True
            else:
                message["embeds"] = False
            if "stickers" in message.keys():
                if message["stickers"] != []:
                    for sticker in message["stickers"]:
                        sticker["message_id"] = message["id"]
                        root_dict["stickers"].append(sticker)
                    message["stickers"] = True
                else:
                    message["stickers"] = False
            if message["reactions"] != []:
                for reaction in message["reactions"]:
                    reaction["message_id"] = message["id"]
                    root_dict["reactions"].append(reaction)
                message["reactions"] = True
            else:
                message["reactions"] = False
            if message["mentions"] != []:
                for mention in message["mentions"]:
                    mention["message_id"] = message["id"]
                    root_dict["mentions"].append(mention)
                message["mentions"] = True
            else:
                message["mentions"] = False
            if "reference" in message.keys():
                message["reference"] = json.dumps(message["reference"])
            else:
                message["reference"] = ""
            root_dict["messages"].append(message)
    return root_dict
