from ExportDiscord import ExportDiscord
import os
ex_dis = ExportDiscord(os.getcwd() + "/colony_discord_guild.sqlite")
ex_dis.create_raw_json_tables()
ex_dis.process_json_files("/home/paul/Projects/DiscordScraping/Colony")
