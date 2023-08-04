import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from pprint import pprint
import os
import glob
import json
import numpy
import sqlalchemy

base_directory = "/home/paul/Projects/exports"

# Recursively find all JSON files in the directory and its subdirectories
json_files = glob.glob(os.path.join(base_directory, '**/*.json'), recursive=True)

engine = create_engine('sqlite:///your_database.db')
# engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

for json_file_path in json_files:
    guilds = []
    channels = []
    messages = []
    # Parts of a message
    authors = {}
    roles = []
    attachments = []
    embeds = []
    stickers = []
    reactions = []
    mentions = []
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    guilds.append(data["guild"])
    data["channel"]["guild_id"] = data["guild"]["id"]
    channels.append(data["channel"])
    for message in data["messages"]:
        if message["author"]["roles"] != []:
            for role in message["author"]["roles"]:
                role["user_id"] = message["author"]
                roles.append(role)
        del message["author"]["roles"]   
        authors[message["author"]["id"]] = message["author"]
        message["author"] = message["author"]["id"]
        if message["attachments"] != []:
            for attachment in message["attachments"]:
                attachment["message_id"] = message["id"]
                attachments.append(attachment)
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
                embeds.append(embed)
            message["embeds"] = True
        else:
            message["embeds"] = False
        if message["stickers"] != []:
            for sticker in message["stickers"]:
                sticker["message_id"] = message["id"]
                stickers.append(sticker)
            message["stickers"] = True
        else:
            message["stickers"] = False
        if message["reactions"] != []:
            for reaction in message["reactions"]:
                reaction["message_id"] = message["id"]
                reactions.append(reaction)
            message["reactions"] = True
        else:
            message["reactions"] = False
        if message["mentions"] != []:
            for mention in message["mentions"]:
                mention["message_id"] = message["id"]
                mentions.append(mention)
            message["mentions"] = True
        else:
            message["mentions"] = False
        if "reference" in message.keys():
            message["reference"] = json.dumps(message["reference"])
        else:
            message["reference"] = ""
        messages.append(message)
    pprint(f"Indexed Channel{channels[0]['name']}")
    df = pd.DataFrame(guilds)
    df.to_sql('guilds', engine, if_exists='append', index=False)
    df2 = pd.DataFrame(channels)
    df2.to_sql('channels', engine, if_exists='append', index=False)
    df = pd.DataFrame(  list(authors.values())  )
    df.to_sql('authors', engine, if_exists='append', index=False)
    df = pd.DataFrame(  attachments  )
    df.to_sql('attachments', engine, if_exists='append', index=False)
    try:
        df = pd.DataFrame(  stickers  )
        df.to_sql('stickers', engine, if_exists='append', index=False)
    except Exception as e:
        print("Issue with stickets")    
        # print(f"An error occurred: {e}")
    df = pd.DataFrame(  reactions  )
    df.to_sql('reactions', engine, if_exists='append', index=False, dtype={"emoji": sqlalchemy.types.JSON})
    df = pd.DataFrame(  embeds  )
    df.to_sql('embeds', engine, if_exists='append', index=False, dtype={
        "author"   : sqlalchemy.types.JSON,
        "thumbnail": sqlalchemy.types.JSON,
        "image"   : sqlalchemy.types.JSON,
        "images"   : sqlalchemy.types.JSON,
        "fields"   : sqlalchemy.types.JSON,
        "footer"   : sqlalchemy.types.JSON
    })
    df = pd.DataFrame(  messages  )
    df.to_sql('messages', engine, if_exists='append', index=False)
        