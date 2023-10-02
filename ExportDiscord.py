from string import Template
import psycopg2
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
import copy

class ExportDiscord():
    def __init__(
        self, 
        db_select="sqlite",
        db_url="./discord_guild_export.sqlite"
    ):
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
        self.db_url = db_url
        print(self.db_url)
        self.db_select = db_select
        if(db_select == "sqlite"):
            self.con = sqlite3.connect(self.db_url)
            # self.con = sqlite3.connect(':memory:')
        elif(db_select == "postgres"):
            self.con = psycopg2.connect(dsn=db_url)
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
        print(f"Running process_discord_json")
        root_dict = {}
        root_dict["guilds"] = []
        root_dict["channels"] = []
        root_dict["messages"] = []
        # Parts of a message
        authors_dict = {}
        root_dict["authors"] = []
        root_dict["roles"] = []
        root_dict["attachments"] = []
        root_dict["embeds"] = []
        root_dict["stickers"] = []
        root_dict["reactions"] = []
        root_dict["mentions"] = []
        root_dict["roles_metadata"] = []
        with open(json_file_path, 'r') as json_file:
            try:
                # print(f"Processing {json_file}")
                data = json.load(json_file)
            except Exception as e:
                return False
        if("guild" not in data):
            return False
        root_dict["guilds"].append(data["guild"])
        data["channel"]["guild_id"] = data["guild"]["id"]
        root_dict["channels"].append(data["channel"])
        for message in data["messages"]:
            message["author_id"] = message["author"]["id"]
            authors_dict[message["author"]["id"]] = message["author"]
            message["channel_id"] = data["channel"]["id"]
            if "roles" in message["author"].keys():
                # TODO this does not work
                if message["author"]["roles"] != []:
                    for role in message["author"]["roles"]:
                        role["user_id"] = message["author"]
                        role["author_id"] = message["author"]["id"]
                        role["author_guild_id"] = message["author"]["id"] + "-" + data["guild"]["id"]
                        role["guild_id"] = data["guild"]["id"]
                        root_dict["roles"].append(role)
                del message["author"]["roles"]   
            if message["attachments"] != []:
                for attachment in message["attachments"]:
                    attachment["message_id"] = message["id"]
                    attachment["message_id"] = message["id"]
                    attachment["guild_id"] = data["guild"]["id"]
                    attachment["author_id"] = message["author"]["id"] 
                    attachment["author_guild_id"] = data["guild"]["id"] + "-" + message["author"]["id"]
                    attachment["guild_id"] = data["guild"]["id"]
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
                    reaction["author_id"] = message["author"]["id"]
                    reaction["author_guild_id"] = message["author"]["id"] + "-" + data["guild"]["id"]
                    reaction["guild_id"] = data["guild"]["id"]
                    reaction["channel_id"] = data["channel"]["id"]
                    root_dict["reactions"].append(reaction)
                message["reactions"] = True
            else:
                message["reactions"] = False
            if message["mentions"] != []:
                for mention in message["mentions"]:
                    mention["message_id"] = message["id"]
                    mention["author_id"] = message["author"]["id"]
                    mention["author_guild_id"] = message["author"]["id"] + "-" + data["guild"]["id"]
                    mention["guild_id"] = data["guild"]["id"]
                    mention["channel_id"] = data["channel"]["id"]
                    root_dict["mentions"].append(mention)
                message["mentions"] = True
            else:
                message["mentions"] = False
            if "reference" in message.keys():
                message["reference"] = json.dumps(message["reference"])
            else:
                message["reference"] = ""
            message["author_guild_id"] = data["guild"]["id"] + "-" + message["author"]["id"]
            message["author"] = message["author"]["id"]
            message["guild_id"] = data["guild"]["id"]
            root_dict["messages"].append(message)
        for author in authors_dict.values(): 
            tmp_author = author
            tmp_author["guild_id"] = data["guild"]["id"] 
            tmp_author["author_id"] = tmp_author["id"]
            tmp_author["author_guild_id"] = tmp_author["id"] + "-" + data["guild"]["id"] 
            root_dict["authors"].append(author)
        print(f"Done Running process_discord_json")
        return root_dict

    def create_raw_json_table(self, table_name):
        sqlite_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name}_t (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_json JSON
            )
        '''
        postgres_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name}_t (
                id serial PRIMARY KEY,
                raw_json JSON
            )
        '''
        if (self.db_select == "sqlite"):
            query = sqlite_query
        elif (self.db_select == "postgres"):
            query = postgres_query
        # print(query)
        retries = 0
        retry_delay=0.3
        while retries < 3:
            try:
                self.cur.execute(query)# .fetchall()
                # self.cur.fetchall()
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
            "mentions",
            "roles_metadata"
        ] 
        for tmp_table_name in raw_table_names:
            self.create_raw_json_table("raw_" + tmp_table_name)

    def json_data_to_sql(self, guild_data):
        print(f"json_data_to_sql Inserting\n {guild_data['channels']}\n\n")
        for tbd_table_name in guild_data.keys():
            print(f"tbd_table_name = {tbd_table_name}")
            print( len( guild_data[tbd_table_name] )  )
            for tbd_row in guild_data[tbd_table_name]:
                retries = 0
                max_retries = 3
                retry_delay = 0.3
                while retries < max_retries:
                    try:
                        postgres_insert_query = f"""
                            INSERT INTO raw_{tbd_table_name}_t (raw_json) VALUES (%s)
                        """
                        sqlite_insert_query = f"""
                            INSERT OR IGNORE INTO raw_{tbd_table_name}_t (raw_json) VALUES (?)
                        """
                        if (self.db_select == "sqlite"):
                            query = sqlite_insert_query
                        elif (self.db_select == "postgres"):
                            query = postgres_insert_query
                        self.cur.execute(query , (json.dumps(tbd_row), ))# .fetchall()
                        # Uncomment this if getting errors, will reduce memory required
                        # self.con.commit()
                        # print(tbd_row)
                        break
                    except sqlite3.OperationalError as e:
                        if "database is locked" in str(e):
                            retries += 1
                            time.sleep(retry_delay)
                        else:
                            raise
                else:
                    raise Exception("Max retries exceeded")
                self.con.commit()

    def process_json_files(self, base_directory):
        json_files = glob.glob(os.path.join(base_directory, '*.json'), recursive=True)
        for json_file in json_files:
            guild_data = self.process_discord_json(json_file)
            if guild_data != False:
                self.json_data_to_sql(guild_data)

    def save_sqlite_to_disk(self, path):
        disk_conn = sqlite3.connect(path)
        self.con.backup(disk_conn)