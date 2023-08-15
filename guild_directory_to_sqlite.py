from ExportDiscord import ExportDiscord
import os

# We are going to save the sqlite databases in the out directory
directory_name = "out"
if not os.path.exists(directory_name):
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created in the current working directory.")
else:
    print(f"Directory '{directory_name}' already exists in the current working directory.")

path = "/home/paul/Projects/DiscordScraping"
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
for directory in directories:
  # print(os.getcwd() + f"/out/{directory}_discord_guild.sqlite")
  ex_dis = ExportDiscord(os.getcwd() + f"/out/{directory}_discord_guild.sqlite")
  ex_dis.create_raw_json_tables()
  ex_dis.process_json_files(path + "/" + directory)
