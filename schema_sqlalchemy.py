# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Date, TEXT, ForeignKey, BOOLEAN, DateTime, BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dateutil import parser
# engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/orm_test.db"
# engine = create_engine(engine_path, echo=True)

Base = declarative_base()

class Guilds(Base):
   __tablename__ = 'guilds_t'
   id = Column(String, primary_key=True)

   guild_name      = Column(String)
   icon_url        = Column(TEXT)
   un_indexed_json = Column(TEXT)
   def __init__(self, id, guild_name, icon_url, un_indexed_json):
        self.id = id
        self.guild_name = guild_name
        self.icon_url = icon_url
        self.un_indexed_json = un_indexed_json


class Channels(Base):
   __tablename__ = 'channels_t'
   id = Column(String, primary_key=True)
  
   channel_name        = Column(TEXT) 
   channel_type        = Column(TEXT)
   category_id         = Column(TEXT) 
   category            = Column(TEXT) 
   guild_id            = Column(String, ForeignKey('guilds_t.id')) 
   topic               = Column(TEXT) 
   channel_name_length = Column(INTEGER) 
   un_indexed_json     = Column(TEXT) 
   def __init__(self, id, channel_name, channel_type, category_id, 
    category, guild_id, topic, channel_name_length ,un_indexed_json):
      print("Channel Init\n\n")
      self.id                    = id
      self.channel_name          = channel_name
      self.channel_type          = channel_type
      self.category_id           = category_id
      self.category              = category
      self.guild_id              = guild_id
      self.topic                 = topic
      self.channel_name_length   = channel_name_length
      self.un_indexed_json       = un_indexed_json

class Authors(Base):
   __tablename__ = 'authors_t'
   id = Column(String, primary_key=True)
  
   author_id        = Column(String) 
   guild_id         = Column(String, ForeignKey('guilds_t.id')) 
   author_name      = Column(TEXT) 
   nickname         = Column(TEXT) 
   color            = Column(TEXT) 
   isBot            = Column(BOOLEAN) 
   avatarUrl        = Column(TEXT) 
   un_indexed_json  = Column(TEXT) 
   def __init__(self, id, author_id, guild_id, author_name, nickname, color, isBot, 
      avatarUrl, un_indexed_json  ):
      self.id                = id
      self.author_id         = author_id  
      self.guild_id          = guild_id  
      self.author_name       = author_name
      self.nickname          = nickname
      self.color             = color
      self.isBot             = isBot
      self.avatarUrl         = avatarUrl
      self.un_indexed_json   = un_indexed_json

class Messages(Base):
   __tablename__ = 'messages_t'
   id = Column(String, primary_key=True)
  
   guild_id             = Column(String, ForeignKey('guilds_t.id')) 
   attachments          = Column(TEXT)
   author_id            = Column(String) 
   author_guild_id      = Column(String, ForeignKey('authors_t.id')) 
   channel_id           = Column(String, ForeignKey('channels_t.id')) 
   msg_content          = Column(TEXT) 
   msg_content_length   = Column(INTEGER) 
   is_bot               = Column(BOOLEAN) 
   is_pinned            = Column(BOOLEAN) 
   mentions             = Column(BOOLEAN) 
   msg_type             = Column(TEXT) 
   msg_timestamp        = Column(DateTime) 
   msg_timestamp_edited = Column(DateTime) 
   un_indexed_json      = Column(TEXT) 
   def __init__(self, id, guild_id, attachments, author_id, 
      author_guild_id, channel_id, content, content_length,
      is_bot, is_pinned, mentions, msg_type,
      msg_timestamp, msg_timestamp_edited, un_indexed_json):
      self.id                   = id
      self.guild_id             = guild_id
      self.attachments          = attachments
      self.author_id            = author_id
      self.author_guild_id      = author_guild_id
      self.channel_id           = channel_id
      self.content              = content
      self.content_length       = int(content_length)
      self.msg_timestamp        = msg_timestamp
      self.is_bot               = is_bot
      self.is_pinned            = is_pinned
      self.mentions             = mentions
      self.msg_type             = msg_type
      self.msg_timestamp        = parser.parse(msg_timestamp)
      if (msg_timestamp_edited != None):
         print(msg_timestamp_edited)
         self.msg_timestamp_edited = parser.parse(msg_timestamp_edited)
      else:
         self.msg_timestamp_edited = datetime(1970,1,1)
      self.un_indexed_json      = un_indexed_json

class Attachments(Base):
   __tablename__ = 'attachments_t'
   id = Column(String, primary_key=True)
  
   attachment_url      = Column(TEXT) 
   file_extension      = Column(TEXT) 
   file_size_bytes     = Column(BIGINT) 
   message_id          = Column(TEXT, ForeignKey('messages_t.id')) 
   author_guild_id     = Column(TEXT, ForeignKey('authors_t.id')) 
   guild_id            = Column(String, ForeignKey('guilds_t.id')) 
   un_indexed_json     = Column(TEXT) 
   def __init__(self, id, attachment_url, file_extension, file_size_bytes,
      message_id, author_guild_id, guild_id, un_indexed_json  ):
      self.id = id
      self.attachment_url      = attachment_url  
      self.file_extension      = file_extension  
      self.file_size_bytes     = file_size_bytes
      self.message_id          = message_id
      self.author_guild_id     = author_guild_id
      self.guild_id            = guild_id
      self.un_indexed_json     = un_indexed_json

class Reactions(Base):
   __tablename__ = 'reactions_t'
   id = Column(String, primary_key=True)
  
   message_id         = Column(String, ForeignKey('messages_t.id')) 
   author_guild_id    = Column(String, ForeignKey('authors_t.id')) 
   channel_id         = Column(String, ForeignKey('channels_t.id')) 
   guild_id           = Column(String, ForeignKey('guilds_t.id')) 
   reaction_count     = Column(INTEGER) 
   emoji_id           = Column(String) 
   emoji_code         = Column(String) 
   emoji_name         = Column(String)
   emoji_json         = Column(TEXT) 
   un_indexed_json    = Column(TEXT) 
   def __init__(self, id, message_id, author_guild_id, channel_id, guild_id, count, 
      emoji_id, emoji_code, emoji_name, emoji_json, un_indexed_json):
      self.id               = id  
      self.message_id       = message_id  
      self.author_guild_id  = author_guild_id
      self.channel_id       = channel_id
      self.guild_id         = guild_id
      self.count            = count
      self.emoji_id         = emoji_id
      self.emoji_code       = emoji_code
      self.emoji_name       = emoji_name
      self.emoji_json       = emoji_json
      self.un_indexed_json  = un_indexed_json

class Roles(Base):
   __tablename__ = 'roles_t'
   id = Column(String, primary_key=True)
      
   role_id             = Column(String) 
   guild_id            = Column(String) # ForeignKey('guilds_t.id')) 
   author_guild_id     = Column(String) 
   name                = Column(TEXT) 
   position            = Column(BIGINT) 
   un_indexed_json     = Column(TEXT) 
   def __init__(self, id, role_id, guild_id, author_guild_id, name, position, un_indexed_json):
        self.id = id
        self.role_id = role_id
        self.guild_id = guild_id
        self.author_guild_id = author_guild_id
        self.name = name
        self.position = position
        self.un_indexed_json = un_indexed_json

class Mentions(Base):
   __tablename__ = 'mentions_t'
   id = Column(String, primary_key=True)

   message_id            = Column(String) # , ForeignKey('messages_t.id') 
   guild_id              = Column(String, ForeignKey('guilds_t.id')) 
   author_guild_id       = Column(String, ForeignKey('authors_t.id')) 
   channel_id            = Column(String, ForeignKey('channels_t.id')) 
   def __init__(self, id, message_id, guild_id, author_guild_id, channel_id):
        self.id = id
        self.message_id = message_id
        self.guild_id = guild_id
        self.author_guild_id = author_guild_id
        self.channel_id = channel_id

# Base.metadata.create_all(engine)
# session = Session(engine)