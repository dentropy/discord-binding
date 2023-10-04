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

print(f'guild_directory_path = {os.environ.get("guild_directory_path") }')

path = str(  os.environ.get("guild_directory_path")  )
directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
print("\ndirectories")
print(directories)
for directory in directories:

  # print(os.getcwd() + f"/out/{directory}_discord_guild.sqlite")

  if(os.environ.get("allow_sqlite_in_memory") == "True"):
    ex_dis = ExportDiscord(  
      "sqlite",
      ":memory:" 
    )
  else:
    if(os.environ.get("db_select") == "sqlite"):
      ex_dis = ExportDiscord(
        os.environ.get("db_select"),
        os.getcwd() + f"/out/{directory}_discord_guild.sqlite"
      )
    else:       
      ex_dis = ExportDiscord(
        os.environ.get("db_select"),
        os.environ.get("db_url")
      )
  ex_dis.create_raw_json_tables()
  ex_dis.process_json_files(path + "/" + directory)
  if(os.environ.get("allow_sqlite_in_memory") == "True"):
    ex_dis.save_sqlite_to_disk(os.getcwd() + f"/out/{directory}_discord_guild.sqlite")
