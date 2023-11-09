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
from psycopg2.extras import execute_batch
import datetime 
import uuid
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


    def test_connection(self):
        try:
            # Execute a simple SQL query (e.g., select the current date)
            self.cur.execute("SELECT current_date")
            # Fetch the result (in this case, a single date)
            result = self.cur.fetchone()
            pprint(result)
            return True
        except:
            return False
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

    def process_discord_json(self, data):
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
        if("guild" not in data):
            return False
        root_dict["guilds"].append(data["guild"])
        data["channel"]["guild_id"] = data["guild"]["id"]
        root_dict["channels"].append(data["channel"])
        for message in data["messages"]:
            message["author_id"] = copy.deepcopy(message["author"]["id"])
            message["isBot"] = message["author"]["isBot"]
            authors_dict[message["author"]["id"]] = message["author"]
            message["channel_id"] = data["channel"]["id"]
            if "roles" in message["author"].keys():
                # TODO this does not work
                for role in message["author"]["roles"]:
                    role["id"] = data["guild"]["id"]
                    role["guild_id"] = data["guild"]["id"]
                    role["author_guild_id"] = data["guild"]["id"] + "-" + message["author"]["id"]
                    root_dict["roles"].append(role)
            if message["attachments"] != []:
                for attachment in message["attachments"]:
                    attachment["message_id"] = message["id"]
                    attachment["message_id"] = message["id"]
                    attachment["guild_id"] = data["guild"]["id"]
                    attachment["author_id"] = message["author"]["id"] 
                    attachment["author_guild_id"] = message["author"]["id"] + "-" + data["guild"]["id"]
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
            message["author_guild_id"] = message["author"]["id"] + "-" + data["guild"]["id"]
            message["author"] = message["author"]["id"]
            message["guild_id"] = data["guild"]["id"]
            root_dict["messages"].append(message)
        # print("\nauthors_dict.values()")
        # pprint(len ( authors_dict.keys())  )
        for author in authors_dict.keys(): 
            tmp_author = authors_dict[author]
            tmp_author["guild_id"] = data["guild"]["id"] 
            tmp_author["author_id"] = tmp_author["id"]
            tmp_author["author_guild_id"] = tmp_author["id"] + "-" + data["guild"]["id"] 
            # pprint(tmp_author["author_guild_id"])
            root_dict["authors"].append(tmp_author)
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
        retries = 0
        retry_delay=0.3
        while retries < 3:
            try:
                self.cur.execute(query)# .fetchall()
                # self.cur.fetchall()
                if(self.db_select == "postgres"):
                    self.con.commit()
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
        return True

    def create_sql_tables(self):
        from postgres_schema import create_table_queries
        for tmp_query in create_table_queries:
            # pprint(tmp_query)
            self.cur.execute(tmp_query)
            self.con.commit()
        return True

    def json_data_to_json_sql(self, guild_data):
        print(f"json_data_to_json_sql Inserting\n {guild_data['channels']}\n\n")
        for tbd_table_name in guild_data.keys():
            postgres_insert_query = f"""
                INSERT INTO raw_{tbd_table_name}_t (raw_json) VALUES (%s)
            """
            sqlite_insert_query = f"""
                INSERT OR IGNORE INTO raw_{tbd_table_name}_t (raw_json) VALUES (?)
            """
            print(f"tbd_table_name = {tbd_table_name}")
            print( len( guild_data[tbd_table_name] )  )
            insert_args = []
            for tbd_row in guild_data[tbd_table_name]:
                if (self.db_select == "sqlite"):
                    query = sqlite_insert_query
                elif (self.db_select == "postgres"):
                    query = postgres_insert_query
                insert_args.append(  [ json.dumps(tbd_row) ]  )
                # (query , (json.dumps(tbd_row), ))# .fetchall()
                # I should use self.cur.executemany
                # Uncomment this if getting errors, will reduce memory required
                # self.con.commit()
                # print(tbd_row)
                # pprint(insert_args)
            execute_batch(self.cur, query, insert_args)
        self.con.commit()

    def json_data_to_sql(self, discord_data):
        pprint("json_data_to_sql")
        if type(discord_data) == type([]):
            pprint(len(discord_data))
        if type(discord_data) == type({}):
            pprint(discord_data.keys())
        # Guilds
        # pprint(discord_data["guilds"])
        query = """
        INSERT INTO guilds_t (id, guild_name, iconUrl, un_indexed_json)
        VALUES (%s, %s, %s, %s) 
        on conflict on constraint guilds_t_pkey do nothing;
        """
        insert_args = [[
            discord_data["guilds"][0]["id"],
            discord_data["guilds"][0]["name"],
            discord_data["guilds"][0]["iconUrl"],
            json.dumps(discord_data["guilds"][0])
        ]]
        execute_batch(self.cur, query, insert_args)
        self.con.commit()
        # Channels
        query = """
        INSERT INTO channels_t (
            id, 
            channel_name, 
            channel_type, 
            categoryId,
            category,
            guild_id,
            topic,
            channel_name_length,
            un_indexed_json
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        on conflict (id) do nothing;
        """
        # pprint("Test Channels")
        # pprint(discord_data["channels"])
        insert_args = [[
            discord_data["channels"][0]["id"],
            discord_data["channels"][0]["name"],
            discord_data["channels"][0]["type"],
            discord_data["channels"][0]["categoryId"],
            discord_data["channels"][0]["category"],
            discord_data["channels"][0]["guild_id"],
            discord_data["channels"][0]["topic"],
            str(  len(discord_data["channels"][0]["name"])  ),
            json.dumps(discord_data["channels"][0])
        ]]
        execute_batch(self.cur, query, insert_args)
        self.con.commit()
        # Messages
        # pprint("Test Messages")
        # pprint(discord_data["messages"][0])
        query = """
        INSERT INTO messages_t (
            id           ,
            guild_id     ,
            attachments  ,
            author_id   , -- 4
            author_guild_id,
            channel_id   ,
            content      ,
            -- interaction  ,
            isBot        ,
            isPinned     , -- 8
            mentions     ,
            msg_type     ,
            msg_timestamp    ,
            msg_timestampEdited , -- 12
            content_length ,
            un_indexed_json -- 14
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s
        )
        on conflict on constraint messages_t_pkey do nothing
        ;
        """
        if len(discord_data["messages"]) != 0:
            messages_list = []
            for message in discord_data["messages"]:
                insert_data = [
                    message["id"], # 1
                    message["guild_id"], # 2
                    str (  message["attachments"]  ), # 3
                    message["author"], # 4
                    message["author_guild_id"], # 5
                    message["channel_id"], # 6
                    message["content"], # 7
                    # message["interaction"],
                    message["isBot"],
                    message["isPinned"], # 8
                    message["mentions"],
                    message["type"],
                    message["timestamp"],
                    message["timestampEdited"],
                    str(  len(message["content"])  ),
                    json.dumps(message)
                ]
                messages_list.append(tuple ( insert_data) )
            execute_batch(self.cur, query, messages_list)
            self.con.commit()
            # Authors
            # pprint("Authors Test")
            # pprint(discord_data["authors"][0])
            query = """
            INSERT INTO authors_t (
                id, 
                author_id,
                guild_id,
                author_name,
                nickname,       -- 5 
                color,
                isBot,
                avatarUrl,
                un_indexed_json -- 9
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s
            ) 
            on conflict (id) do nothing;
            """
            authors_list = []
            for author in discord_data["authors"]:
                # pprint(author["author_guild_id"])
                authors_list.append([
                    author["author_guild_id"], # 1
                    author["author_id"],       # 2
                    author["guild_id"],        # 3
                    author["name"],             # 4
                    author["nickname"],         # 5
                    author["color"],            # 6
                    author["isBot"],            # 7
                    author["avatarUrl"],        # 8 
                    json.dumps(author)          # 9
                ])
            # pprint("authors_list")
            # pprint(authors_list)
            execute_batch(self.cur, query, authors_list)
            self.con.commit()
        # Reactions
        if len(discord_data["reactions"]) != 0:
            query = """
            INSERT INTO reactions_t (
                id        , -- 1
                message_id         ,
                author_guild_id    ,
                channel_id         ,
                guild_id           ,
                count              ,
                emoji_id           ,
                emoji_code         ,
                emoji_name         ,
                emoji_json         , -- 10
                un_indexed_json
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s
            )
            on conflict (id) do nothing;
            """
            reactions_list = []
            for reaction in discord_data["reactions"]:
                reactions_list.append([
                    reaction['message_id'] + "-" + reaction['emoji']['code'] + "-" + str(reaction["count"]),
                    reaction["message_id"],
                    reaction["author_guild_id"],
                    reaction["channel_id"], # 4
                    reaction["guild_id"],
                    reaction["count"],
                    reaction["emoji"]["id"],
                    reaction["emoji"]["code"], # 8
                    reaction["emoji"]["name"],
                    json.dumps(reaction["emoji"]),
                    json.dumps(reaction) # 11
                ])
            execute_batch(self.cur, query, reactions_list)
            self.con.commit()
        # Attachments
        if len(discord_data["attachments"]) != 0:
            query = """
            INSERT INTO attachments_t (
                id                     , -- 1
                attachment_url         ,
                file_extension         ,
                fileSizeBytes          , -- 4
                message_id             ,
                author_guild_id        ,
                guild_id               ,
                un_indexed_json        -- 8
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            on conflict (id) do nothing;
            """
            attachments_list = []
            for attachment in discord_data["attachments"]:
                attachments_list.append([
                    attachment["id"],
                    attachment["url"],
                    attachment["url"].split(".")[-1],
                    attachment["fileSizeBytes"], # 4
                    attachment["message_id"],
                    attachment["author_guild_id"], # TODO missing channel_id
                    attachment["guild_id"],
                    json.dumps(reaction) # 8
                ])
            execute_batch(self.cur, query, attachments_list)
            self.con.commit()
        # Roles
        # pprint("Test Roles")
        # pprint(discord_data["roles"][0])
        if(len(discord_data["roles"]) != 0) :
            query = """
            INSERT INTO roles_t (
                id              , -- 1
                role_id         ,
                guild_id        ,
                author_guild_id ,
                name            ,
                position        ,
                un_indexed_json -- 7
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s
            )
            on conflict (id) do nothing;
            """
            roles_list = []
            for role in discord_data["roles"]:
                roles_list.append([
                    role["author_guild_id"] + "-" + role["id"], # 1
                    role["id"],
                    role["guild_id"],
                    role["author_guild_id"],
                    role["name"],
                    role["position"],
                    json.dumps(role) # 7
                ])
            execute_batch(self.cur, query, roles_list)
            self.con.commit()
        # mentions
        # pprint("Test Mentions")
        # pprint(discord_data["mentions"][0])
        if(len(discord_data["mentions"]) != 0) :
            query = """
            INSERT INTO mentions_t (
                id,
                message_id,
                guild_id,
                author_guild_id
            )
            VALUES (
                %s, %s, %s, %s
            )
            on conflict (id) do nothing;
            """
            mentions_list = []
            for mention in discord_data["mentions"]:
                mentions_list.append([
                    mention["author_guild_id"] + "-" + mention["message_id"],
                    mention["id"],
                    mention["guild_id"],
                    mention["author_guild_id"]
                    # TODO, add channel_ID
                ])
            execute_batch(self.cur, query, mentions_list)
            self.con.commit()
        # embeds
        # stickers
    def process_json_files(self, base_directory):
        json_files = glob.glob(os.path.join(base_directory, '*.json'), recursive=True)
        for json_file in json_files:
            with open(json_file, 'r') as json_file:
                try:
                    # print(f"Processing {json_file}")
                    data = json.load(json_file)
                except Exception as e:
                    return False
            guild_data = self.process_discord_json(data)
            if guild_data != False:
                self.json_data_to_json_sql(guild_data)

    def save_sqlite_to_disk(self, path):
        disk_conn = sqlite3.connect(path)
        self.con.backup(disk_conn)