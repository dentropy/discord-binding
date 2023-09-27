from ExportDiscord import ExportDiscord
import os
from dotenv import load_dotenv
load_dotenv()

# We are going to save the sqlite databases in the out directory
directory_name = "out"
if not os.path.exists(directory_name):
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created in the current working directory.")
else:
    print(f"Directory '{directory_name}' already exists in the current working directory.")

path = str(  os.environ.get("guild_directory_path")  )
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
for directory in directories:
  print(os.getcwd() + f"/out/{directory}_discord_guild.sqlite")
  ex_dis = ExportDiscord(
    "sqlite",
    os.getcwd() + f"/out/{directory}_discord_guild.sqlite"
  )
  ex_dis.create_raw_json_tables()
  ex_dis.process_json_files(path + "/" + directory)
  ex_dis.save_sqlite_to_disk(os.getcwd() + f"/out/{directory}_discord_guild.sqlite")
