import process_discord_json

guild_data = process_discord_json.process_discord_json( "/home/paul/Projects/DiscordScraping/Colony")
from ExportDiscord import ExportDiscord
ex_dis = ExportDiscord()
guild_data.keys()
for tbd_table in guild_data.keys():
    ex_dis.create_raw_json_table("raw_" + tbd_table)

import json
import sqlite3
import time
for tbd_table_name in guild_data.keys():
    for tbd_row in guild_data[tbd_table_name]:
        retries = 0
        max_retries = 3
        retry_delay = 0.3
        while retries < max_retries:
            try:
                ex_dis.cur.execute( f'INSERT INTO raw_{tbd_table_name}_t (raw_json) VALUES (?)', (json.dumps(tbd_row),)).fetchall()
                ex_dis.con.commit()
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
