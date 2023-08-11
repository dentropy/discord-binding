import os
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.types import JSON
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/orm_test.db"
# engine = create_engine(engine_path, echo=True)

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

Base = declarative_base()

class RawGuilds(Base):
   __tablename__ = 'raw_guilds_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)
   def __init__(self, raw_json):
        self.raw_json = raw_json


class RawChannels(Base):
   __tablename__ = 'raw_channels_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)
   def __init__(self, raw_json):
        self.raw_json = raw_json

class RawMessages(Base):
   __tablename__ = 'raw_messages_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)
   def __init__(self, raw_json):
        self.raw_json = raw_json

class RawAttachments(Base):
   __tablename__ = 'raw_attachments_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)
   def __init__(self, raw_json):
        self.raw_json = raw_json

class RawReactions(Base):
   __tablename__ = 'raw_reactions_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)

class RawAuthors(Base):
   __tablename__ = 'raw_authors_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)


class RawRoles(Base):
   __tablename__ = 'raw_roles_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)


class RawMentions(Base):
   __tablename__ = 'raw_mentions_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)

class RawStickers(Base):
   __tablename__ = 'raw_stickers_t'
   id = Column(Integer, primary_key=True, autoincrement=True)
   raw_json = Column(JSON)

Base.metadata.create_all(engine)
session = Session(engine)