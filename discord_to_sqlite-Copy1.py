import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from pprint import pprint
import os
import glob
import json
import numpy
base_directory = "/home/paul/Projects/exports"

# Recursively find all JSON files in the directory and its subdirectories
json_files = glob.glob(os.path.join(base_directory, '**/*.json'), recursive=True)

engine = create_engine('sqlite:///your_database.db')

guilds = []
channels = []
# Print the list of JSON files
pprint(json_files)
for json_file_path in json_files:
  with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)
  guilds.append(data["guild"])
  data["channel"]["guild_id"] = data["guild"]["id"]
  channels.append(data["channel"])
  message_df = pd.DataFrame(data["messages"])
  # message_df = pd.json_normalize(data["messages"])
  # dtypes = numpy.dtype(
  # [
  #     ('id'        , str), 
  #     ('type'      , object), 
  #     ('timestamp' , numpy.datetime64),
  #     ('timestampEdited'      ,numpy.datetime64),
  #     ('callEndedTimestamp'      , numpy.datetime64),
  #     ('isPinned'      , numpy.bool),
  #     ('content'      , object),
  #     ('author'      , object),
  #     ('attachments'      , object),
  #     ('embeds'      , object),
  #     ('stickers'      , object),
  #     ('reactions'      , object),
  #     ('mentions'      , object)]
  # )
  # message_df = pd.DataFrame(data["messages"], dtype=dtypes)
  # message_df = pd.DataFrame(data["messages"],
  #   dtype=[
  #     ('id'        , 'object'), 
  #     ('type'      , 'object'), 
  #     ('timestamp' , 'datetime64'),
  #     ('timestampEdited'      , 'datetime64'),
  #     ('callEndedTimestamp'      , 'datetime64'),
  #     ('isPinned'      , 'bool'),
  #     ('content'      , 'object'),
  #     ('author'      , 'object'),
  #     ('attachments'      , 'object'),
  #     ('embeds'      , 'object'),
  #     ('stickers'      , 'object'),
  #     ('reactions'      , 'object'),
  #     ('mentions'      , 'object')])
  
  # message_df['guild_id'] = data["guild"]["id"]
  # message_df['channel_id'] = data["channel"]["id"]
  
  
  # pprint(message_df)
  # message_df['author'] = message_df['author'].apply(json.dumps)
  # message_df['attachments'] = message_df['attachments'].apply(json.dumps)
  # message_df['embeds'] = message_df['embeds'].apply(json.dumps)
  # message_df['stickers'] = message_df['stickers'].apply(json.dumps)
  # message_df['reactions'] = message_df['reactions'].apply(json.dumps)
  # message_df['mentions'] = message_df['mentions'].apply(json.dumps)
  message_df.drop(columns='author', inplace=True)
  message_df.drop(columns='attachments', inplace=True)
  message_df.drop(columns='embeds', inplace=True)
  message_df.drop(columns='stickers', inplace=True)
  message_df.drop(columns='reactions', inplace=True)
  message_df.drop(columns='mentions', inplace=True)
  message_df.drop(columns='callEndedTimestamp', inplace=True)
  message_df.drop(columns='timestampEdited', inplace=True)
  message_df.drop(columns='isPinned', inplace=True)
  # message_df.drop(columns='id', inplace=True)
  message_df.drop(columns='type', inplace=True)
  message_df.drop(columns='timestamp', inplace=True)
  # message_df.drop(columns='content', inplace=True)
  # message_df.drop(columns='reference', inplace=True)
  tmp_messages = message_df.to_json()
  pprint(tmp_messages)
  message_df2 = pd.read_json(tmp_messages)
  message_df2.to_sql(f"messages{data['guild']['id']}", engine, if_exists='replace', index=False)
  engine.dispose()


# df = pd.DataFrame(guilds)
# df.to_sql('guilds', engine, if_exists='replace', index=False)
# df2 = pd.DataFrame(channels)
# df2.to_sql('channels', engine, if_exists='replace', index=False)

# # # Step 5: Close the SQLAlchemy engine
# engine.dispose()
