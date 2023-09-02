from string import Template
import subprocess
import json
from glob import glob
import os
from pprint import pprint
# from database import DB, Messages, Users
# from urlextract import URLExtract
import datetime
from pathlib import Path
import sqlite3
# from sqlalchemy import distinct, desc
import time
import glob

class ExportDiscord():
    def __init__(self, sqlite_url="./discord_guild_export.sqlite"):
        """Initialize the ExportKeybase object."""
        # self.extractor = URLExtract()
        # Make folders if they do not exist
        # self.save_dir = save_dir
        # Path(save_dir).mkdir(parents=True, exist_ok=True)
        # Path(f"{self.save_dir}/GitRepos").mkdir(parents=True, exist_ok=True)
        # paths_in_dir = glob(self.save_dir + "/*")
        # files_in_dir = []
        # for path in paths_in_dir:
        #    files_in_dir.append( path.split("/")[-1] )
        self.sqlite_url = sqlite_url
        print(self.sqlite_url)
        self.con = sqlite3.connect(self.sqlite_url)
        self.cur = self.con.cursor()

    def execute_with_retry(self, query, params=None, max_retries=3, retry_delay=0.1):
        retries = 0
        while retries < max_retries:
            try:
                self.cur.execute(query, params).fetchall()
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retries += 1
                    time.sleep(retry_delay)
                else:
                    raise
        else:
            raise Exception("Max retries exceeded")

    def process_discord_json(self, json_file_path):
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
        with open(json_file_path, 'r') as json_file:
            try:
                # print(f"Processing {json_file}")
                data = json.load(json_file)
            except Exception as e:
                return False
        root_dict["guilds"].append(data["guild"])
        data["channel"]["guild_id"] = data["guild"]["id"]
        root_dict["channels"].append(data["channel"])
        for message in data["messages"]:
            message["channel_id"] = data["channel"]["id"]
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

    def create_raw_json_table(self, table_name):
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name}_t (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_json JSON
            )
        '''
        print(query)
        retries = 0
        retry_delay=0.3
        while retries < 3:
            try:
                self.cur.execute(query).fetchall()
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    retries += 1
                    time.sleep(retry_delay)
                else:
                    raise
            return True


    def create_raw_json_tables(self):
        raw_table_names = [
             "guilds",
            "channels",
            "messages",
            "authors",
            "roles",
            "attachments",
            "embeds",
            "stickers",
            "reactions",
            "mentions"
        ] 
        for tmp_table_name in raw_table_names:
            self.create_raw_json_table("raw_" + tmp_table_name)

    def json_data_to_sql(self, guild_data):
        for tbd_table_name in guild_data.keys():
            for tbd_row in guild_data[tbd_table_name]:
                retries = 0
                max_retries = 3
                retry_delay = 0.3
                while retries < max_retries:
                    try:
                        self.cur.execute( f'INSERT INTO raw_{tbd_table_name}_t (raw_json) VALUES (?)', (json.dumps(tbd_row),)).fetchall()
                        self.con.commit()
                        print(tbd_row)
                        break
                    except sqlite3.OperationalError as e:
                        if "database is locked" in str(e):
                            retries += 1
                            time.sleep(retry_delay)
                        else:
                            raise
                else:
                    raise Exception("Max retries exceeded")

    def process_json_files(self, base_directory):
        json_files = glob.glob(os.path.join(base_directory, '*.json'), recursive=True)
        for json_file in json_files:
            guild_data = self.process_discord_json(json_file)
            if guild_data != False:
                self.json_data_to_sql(guild_data)
