from ExportDiscord import ExportDiscord
import os
ex_dis = ExportDiscord(os.getcwd() + "/Arbitrum2.sqlite")
ex_dis.create_raw_json_tables()
ex_dis.process_json_files("/home/paul/Projects/DiscordScraping/Processed/Arbitrum")
