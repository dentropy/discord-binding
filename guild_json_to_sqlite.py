from ExportDiscord import ExportDiscord
import os
from dotenv import load_dotenv
load_dotenv()
guild_path = os.environ.get("guild_path")
db_name = guild_path.split("/")[-1]
# ex_dis = ExportDiscord(os.getcwd() + f"/{db_name}.sqlite")
ex_dis = ExportDiscord(  
  os.environ.get("db_select"),
  os.environ.get("db_url")  
)
ex_dis.create_raw_json_tables()
ex_dis.process_json_files(guild_path)
