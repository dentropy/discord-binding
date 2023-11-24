from string import Template
import psycopg2
import subprocess
import json
from glob import glob
import os
from pprint import pprint
# from database import DB, Messages, Users
# from urlextract import URLExtract
# from sqlalchemy import distinct, desc
from pathlib import Path
import sqlite3
import time
import glob
from psycopg2.extras import execute_batch
import uuid
from sqlalchemy.dialects.postgresql import insert

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
        self.db_select = db_select
        if(db_select == "sqlite"):
            self.con = sqlite3.connect(self.db_url)
            # self.con = sqlite3.connect(':memory:')
            self.cur = self.con.cursor()
        elif(db_select == "postgres"):
            self.con = psycopg2.connect(dsn=db_url)
            self.cur = self.con.cursor()
        elif(db_select == "sqlalchemy"):
            from sqlalchemy import create_engine
            from sqlalchemy.orm import Session, sessionmaker
            engine_path = db_url
            self.engine = create_engine(engine_path, echo=True)
            Session = sessionmaker(bind=self.engine, autoflush=False)
            self.session = Session()
        elif(db_select == "neo4j"):
            from neomodel import db
            self.db = db.set_connection(url=self.db_url)




    def test_connection(self):
        if(self.db_select == "posgres"):
            try:
                # Execute a simple SQL query (e.g., select the current date)
                self.cur.execute("SELECT version();")
                # Fetch the result (in this case, a single date)
                result = self.cur.fetchone()
                pprint(result)
                return True
            except Exception as e:
                print(e)
                return False
        elif(self.db_select == "sqlalchemy"):
            from schemas.sqlalchemy import create_engine
            # [SQLAlchemy Connection Test](https://chat.openai.com/share/f6e511fe-2db5-4de8-aa05-9df38efea672)
            try:
                # Create an engine
                engine = create_engine(self.db_url)

                # Try to connect
                with engine.connect() as connection:
                    # print("Connection successful!")
                    return True
                    
            except Exception as e:
                # print(f"Connection failed! Error: {e}")
                return False
        elif (self.db_select == "neo4j"):
            try:
                from neomodel import db
                db.set_connection(url=self.db_url)
                results, meta = db.cypher_query("RETURN 'Hello World' as message")
                return True
            except Exception as e:
                # print(f"Connection failed! Error: {e}")
                return False
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
        root_dict["replies"] = []
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
            message["author_id"] = message["author"]["id"] # copy.deepcopy(message["author"]["id"])
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
            if "reference" in message.keys():
                reply_msg = {}
                if "messageId" in message["reference"].keys():
                    reply_msg["id"] = message["id"],
                    reply_msg["guild_id"] = data["guild"]["id"],
                    reply_msg["channel_id"] = data["channel"]["id"],
                    reply_msg["author_id"] = message["author"]["id"] 
                    reply_msg["author_guild_id"] = message["author"]["id"] + "-" + data["guild"]["id"]
                    reply_msg["reply_to_channel_id"] = message["reference"]["channelId"]
                    reply_msg["reply_to_message_id"] = message["reference"]["messageId"]
                root_dict["replies"].append(reply_msg)
                message["reference"] = str(message["reference"]["messageId"])
            else:
                message["reference"] = None
            if message["attachments"] != []:
                for attachment in message["attachments"]:
                    attachment["message_id"] = message["id"]
                    attachment["message_id"] = message["id"]
                    attachment["guild_id"] = data["guild"]["id"]
                    attachment["author_id"] = message["author"]["id"] 
                    attachment["author_guild_id"] = message["author"]["id"] + "-" + data["guild"]["id"]
                    attachment["guild_id"] = data["guild"]["id"],
                    attachment["channel_id"] = data["channel"]["id"],
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
        if(self.db_select == "postgres"):
            from schemas.schema_postgres import create_table_queries
            for tmp_query in create_table_queries:
                # pprint(tmp_query)
                self.cur.execute(tmp_query)
                self.con.commit()
            return True
        elif(self.db_select == "sqlalchemy"):
            from schemas.schema_sqlalchemy import Base
            Base.metadata.create_all(self.engine)

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
        # pprint("json_data_to_sql")
        # if type(discord_data) == type([]):
        #     pprint(len(discord_data))
        # if type(discord_data) == type({}):
        #     pprint(discord_data.keys())
        if self.db_select == "postgres":
            if ("guilds" in discord_data):
                print("Guilds Data")
                pprint(discord_data["guilds"])
                query = """
                INSERT INTO guilds_t (id, guild_name, icon_url, un_indexed_json)
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
                category_id,
                category,
                guild_id,
                topic,
                channel_name_length,
                un_indexed_json
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            on conflict (id) do nothing;
            """
            # pprint("\n\nTest Channels")
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
            # pprint("\n\nTest Messages")
            # pprint(discord_data["messages"][0])
            query = """
            INSERT INTO messages_t (
                id           ,
                guild_id     ,
                channel_id   ,
                author_id    ,
                author_guild_id,
                msg_content      ,
                msg_content_length ,
                -- interaction  ,
                attachments  ,
                is_bot       ,
                is_pinned    , -- 10
                mentions     ,
                msg_type     ,
                msg_timestamp,
                msg_timestamp_edited,
                reply_to_message_id,
                un_indexed_json
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            on conflict on constraint messages_t_pkey do nothing
            ;
            """
            if len(discord_data["messages"]) != 0:
                messages_list = []
                for message in discord_data["messages"]:
                    # print(f"\nMessage\n{message}\n\n")
                    # tmp = message["reference"]
                    # print(f"\nreference\n{tmp}\n\n")
                    insert_data = [
                        message["id"], # 1
                        message["guild_id"], # 2
                        message["channel_id"], # 3
                        message["author"], # 4
                        message["author_guild_id"], # 5
                        message["content"], # 6
                        str(  len(message["content"])  ), # 7
                        # message["interaction"],
                        str (  message["attachments"]  ), # 8
                        message["isBot"],
                        message["isPinned"], # 9
                        message["mentions"], # 10
                        message["type"],
                        message["timestamp"],
                        message["timestampEdited"],
                        message["reference"][1:-1],
                        json.dumps(message)
                    ]
                    messages_list.append(tuple ( insert_data) )
                execute_batch(self.cur, query, messages_list)
                self.con.commit()


            query = """
            INSERT INTO message_replies_t (
                id           ,
                guild_id     ,
                channel_id   ,
                author_id   , 
                author_guild_id,
                reply_to_channel_id,
                reply_to_message_id
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s
            )
            on conflict on constraint message_replies_t_pkey do nothing
            ;
            """
            if len(discord_data["replies"]) != 0:
                messages_list = []
                for reply_msg in discord_data["replies"]:
                    print(f"\nMessage Reply\n{reply_msg}\n\n")
                    import uuid
                    random_uuid = uuid.uuid4()
                    insert_data = [
                        reply_msg["id"], # 1
                        reply_msg["guild_id"], # 2
                        reply_msg["channel_id"], # 3
                        reply_msg["author_id"], # 4
                        reply_msg["author_guild_id"], # 5,
                        reply_msg["reply_to_channel_id"], # 6
                        reply_msg["reply_to_message_id"] # 7

                    ]
                    pprint(tuple ( insert_data))
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
                    is_bot,
                    avatar_url,
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
                    reaction_count     ,
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
                    file_size_bytes        , -- 4
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
                        json.dumps(attachment) # 8
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
            # TODO embeds
            # TODO stickers
        if self.db_select == "sqlalchemy":
            from schema_sqlalchemy import Guilds, Channels, Messages, Attachments, Authors, Reactions, Roles, Mentions
            ins = insert(Guilds).values(
                id = discord_data["guilds"][0]["id"],
                guild_name = discord_data["guilds"][0]["name"],
                icon_url = discord_data["guilds"][0]["iconUrl"],
                un_indexed_json = json.dumps(discord_data["guilds"][0])
            ).on_conflict_do_nothing(index_elements=['id'])
            self.session.execute(ins)
            # self.session.commit()
            ins = insert(Channels).values(
                    id = discord_data["channels"][0]["id"],
                    channel_name = discord_data["channels"][0]["name"],
                    channel_type = discord_data["channels"][0]["type"],
                    category_id = discord_data["channels"][0]["categoryId"],
                    category = discord_data["channels"][0]["category"],
                    guild_id = discord_data["channels"][0]["guild_id"],
                    topic = discord_data["channels"][0]["topic"],
                    channel_name_length = len(discord_data["channels"][0]["name"]),
                    un_indexed_json = json.dumps(discord_data["channels"][0])
                ).on_conflict_do_nothing(index_elements=['id'])
            self.session.execute(ins)
            self.session.commit()
            for author in discord_data["authors"]:
                # pprint(author["author_guild_id"])
                ins = insert(Authors).values(
                    id = author["author_guild_id"], # 1
                    author_id = author["author_id"],       # 2
                    guild_id = author["guild_id"],        # 3
                    author_name = author["name"],             # 4
                    nickname = author["nickname"],         # 5
                    color = author["color"],            # 6
                    isBot = author["isBot"],            # 7
                    avatarUrl = author["avatarUrl"],        # 8 
                    un_indexed_json = json.dumps(author)          # 9
                ).on_conflict_do_nothing(index_elements=['id'])
                self.session.execute(ins)
            self.session.commit()
            if len(discord_data["messages"]) != 0:
                messages_list = []
                for message in discord_data["messages"]:
                    self.session.add(Messages(
                        message["id"], # 1
                        message["guild_id"], # 2
                        str (  message["attachments"]  ), # 3
                        message["author"], # 4
                        message["author_guild_id"], # 5
                        message["channel_id"], # 6
                        message["content"], # 7
                        len(message["content"]), # 8
                        # message["interaction"],
                        message["isBot"], # 9
                        message["isPinned"],
                        message["mentions"],
                        message["type"],
                        message["timestamp"],
                        message["timestampEdited"],
                        json.dumps(message)
                    ))
                    self.session.commit()
            if len(discord_data["reactions"]) != 0:
                for reaction in discord_data["reactions"]:
                    self.session.add(Reactions(
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
                    ))
                self.session.commit()
            if len(discord_data["attachments"]) != 0:
                for attachment in discord_data["attachments"]:
                    self.session.add(Attachments(
                        attachment["id"],
                        attachment["url"],
                        attachment["url"].split(".")[-1],
                        attachment["fileSizeBytes"], # 4
                        attachment["message_id"],
                        attachment["author_guild_id"], # TODO missing channel_id
                        attachment["guild_id"],
                        json.dumps(attachment) # 8
                    ))
                self.session.commit()
            # So slow not even worth running, # TODO optimize, maybe do a select for everything then only insert what can actually be inserted
            # if(len(discord_data["roles"]) != 0) :
            #     for role in discord_data["roles"]:
            #         ins = insert(Roles).values(
            #             id = role["author_guild_id"] + "-" + role["id"], # 1
            #             role_id = role["id"],
            #             guild_id = role["guild_id"],
            #             author_guild_id = role["author_guild_id"],
            #             name = role["name"],
            #             position = role["position"],
            #             un_indexed_json = json.dumps(role) # 7
            #         ).on_conflict_do_nothing(index_elements=['id'])
            #         # self.session.add(ins)
            #         self.session.execute(ins)
            #     self.session.commit()
            if(len(discord_data["mentions"]) != 0) :
                for mention in discord_data["mentions"]:
                    # print(f"\n\nMention\n\n{mention}\n\n")
                    # print(mention["channel_id"])
                    # print(mention["id"])
                    # print("\n\n")
                    values = {
                        'id' : mention["author_guild_id"] + "-" + mention["message_id"],
                        'message_id' : mention["id"],
                        'guild_id' : mention["guild_id"],
                        'author_guild_id' : mention["author_guild_id"],
                        'channel_id' : mention["channel_id"]
                    }
                    print(values)
                    ins = insert(Mentions).values(values).on_conflict_do_nothing(index_elements=['id'])
                    self.session.execute(ins)
                self.session.commit()
            # TODO embeds
            # TODO stickers
        if self.db_select == "neo4j":
            from schemas.schema_neo4j import Guilds, Channels, Authors, Messages, Reactions, Emoji, Replies, Attachments, Mentions
            from neomodel import db
            from dateutil import parser
            db.set_connection(url=self.db_url)
            #with db.transaction:
            # TODO, check if guild is already inserted or not
            guild = Guilds(
                identifier = discord_data["guilds"][0]["id"],
                guild_name = discord_data["guilds"][0]["name"],
                icon_url = discord_data["guilds"][0]["iconUrl"]
            ).save()
            # inserted_guild = Guilds.nodes.get(identifier=discord_data["guilds"][0]["id"])
            channel = Channels(
                identifier = discord_data["channels"][0]["id"],
                channel_name = discord_data["channels"][0]["name"],
                channel_type = discord_data["channels"][0]["type"],
                category_id = discord_data["channels"][0]["categoryId"],
                category = discord_data["channels"][0]["category"],
                # guild_id = discord_data["channels"][0]["guild_id"],
                # discord_topic = discord_data["channels"][0]["topic"],
                channel_name_length = len(discord_data["channels"][0]["name"])
            ).save()
            # inserted_channel = Channels.nodes.get(identifier = discord_data["channels"][0]["id"])
            # pprint(channel)
            # pprint(channel.guild_id)
            channel.guild_id.connect(guild)
            for author in discord_data["authors"]:
                author = Authors(
                    identifier = author["author_guild_id"], # 1
                    author_id = author["author_id"],       # 2
                    # guild_id = author["guild_id"],        # 3
                    author_name = author["name"],             # 4
                    nickname = author["nickname"],         # 5
                    # color = author["color"],            # 6
                    is_bot = author["isBot"],            # 7
                    avatar_url = author["avatarUrl"],        # 8 
                    un_indexed_json = json.dumps(author)          # 9
                ).save()
                author.guild_id.connect(guild)
            if len(discord_data["messages"]) != 0:
                messages_list = []
                for message in discord_data["messages"]:
                    insert_message = (Messages(
                        identifier = message["id"], # 1
                        # guild_id = message["guild_id"], # 2
                        attachments = str (  message["attachments"]  ), # 3
                        # author_id = message["author"], # 4
                        # author_guild_id = message["author_guild_id"], # 5
                        # channel_id = message["channel_id"], # 6
                        msg_content = message["content"], # 7
                        msg_content_length = len(message["content"]), # 8
                        # message["interaction"],
                        is_bot = message["isBot"], # 9
                        isPinned = message["isPinned"],
                        mentions = message["mentions"],
                        msg_type = message["type"],
                        msg_timestamp = parser.parse(message["timestamp"]),
                        # msg_timestamp_edited= parser.parse(message["timestampEdited"])
                    )).save()
                    insert_message.guild_id.connect(guild)
                    # pprint(dir(Authors.nodes))
                    author_to_connect = Authors.nodes.first_or_none(identifier=message["author_guild_id"])
                    # print(f"\n\n{author_to_connect}\n\n")
                    insert_message.author_guild_id.connect(author_to_connect)
                    channel_to_connect = Channels.nodes.first_or_none(identifier=message["channel_id"])
                    # print(f"\n\n{channel_to_connect}\n\n")
                    insert_message.channel_id.connect(channel_to_connect)                   
            if len(discord_data["reactions"]) != 0:
                for reaction in discord_data["reactions"]:
                    insert_message = (Reactions(
                        identifier = reaction['message_id'] + "-" + reaction['emoji']['code'] + "-" + str(reaction["count"]),
                        message_id = reaction["message_id"],
                        # author_guild_id = reaction["author_guild_id"],
                        # channel_id = reaction["channel_id"], # 4
                        # guild_id = reaction["guild_id"],
                        reaction_count = reaction["count"],
                        emoji_id = reaction["emoji"]["id"],
                        emoji_code = reaction["emoji"]["code"], # 8
                        emoji_name = reaction["emoji"]["name"],
                        emoji_json = json.dumps(reaction["emoji"])
                    )).save()
                    insert_message.guild_id.connect(guild)
                    # pprint(dir(Authors.nodes))
                    author_to_connect = Authors.nodes.first_or_none(identifier=message["author_guild_id"])
                    # print(f"\n\n{author_to_connect}\n\n")
                    insert_message.author_guild_id.connect(author_to_connect)
                    channel_to_connect = Channels.nodes.first_or_none(identifier=message["channel_id"])
                    # print(f"\n\n{channel_to_connect}\n\n")
                    insert_message.channel_id.connect(channel_to_connect)
                    
                    # TODO Create a reaction type and link to it
            if len(discord_data["attachments"]) != 0:
                for attachment in discord_data["attachments"]:
                    insert_message = (Attachments(
                        identifier = attachment["id"],
                        attachment_url = attachment["url"],
                        file_extension = attachment["url"].split(".")[-1],
                        file_size_bytes = attachment["fileSizeBytes"], # 4
                        # message_id = attachment["message_id"],
                        # author_guild_id = attachment["author_guild_id"], # TODO missing channel_id
                        # guild_id = attachment["guild_id"]
                    )).save()
                    insert_message.guild_id.connect(guild)
                    # pprint(dir(Authors.nodes))
                    author_to_connect = Authors.nodes.first_or_none(identifier=message["author_guild_id"])
                    # print(f"\n\n{author_to_connect}\n\n")
                    insert_message.author_guild_id.connect(author_to_connect)
                    # channel_to_connect = Channels.nodes.first_or_none(identifier=message["channel_id"])
                    # print(f"\n\n{channel_to_connect}\n\n")
                    # insert_message.channel_id.connect(channel_to_connect)
                # TODO Create a attachment ending node and link to it
            # TODO roles
            if(len(discord_data["replies"]) != 0) :
                # TODO replies
                for reply in discord_data["mentions"]:
                    insert_message = Mentions(
                        identifier = reply["id"]
                    ).save()
                    insert_message.guild_id.connect(guild)
                    # pprint(dir(Authors.nodes))
                    author_to_connect = Authors.nodes.first_or_none(identifier=message["author_guild_id"])
                    # print(f"\n\n{author_to_connect}\n\n")
                    insert_message.author_guild_id.connect(author_to_connect)
                    channel_to_connect = Channels.nodes.first_or_none(identifier=message["channel_id"])
                    # print(f"\n\n{channel_to_connect}\n\n")
                    insert_message.channel_id.connect(channel_to_connect)

                    # TODO make sure all Relationships are filled, that are not currently
                    
                    # author_to_connect = Authors.nodes.first_or_none(identifier=message["reply_to_author_guild_id"])
                    # insert_message.author_guild_id.connect(author_to_connect)
                    # insert_message.reply_to_author_guild_id.connect(channel_to_connect)
            if(len(discord_data["mentions"]) != 0) :
                for mention in discord_data["mentions"]:
                    # print(f"\n\nMention\n\n{mention}\n\n")
                    # print(mention["channel_id"])
                    # print(mention["id"])
                    # print("\n\n")
                    insert_message = Mentions(
                        identifier = mention["author_guild_id"] + "-" + mention["message_id"]
                    ).save()
                    insert_message.guild_id.connect(guild)
                    # pprint(dir(Authors.nodes))
                    author_to_connect = Authors.nodes.first_or_none(identifier=message["author_guild_id"])
                    # print(f"\n\n{author_to_connect}\n\n")
                    insert_message.author_guild_id.connect(author_to_connect)
                    channel_to_connect = Channels.nodes.first_or_none(identifier=message["channel_id"])
                    # print(f"\n\n{channel_to_connect}\n\n")
                    insert_message.channel_id.connect(channel_to_connect)
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