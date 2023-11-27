from neomodel import (config, db, StructuredNode, BooleanProperty, StringProperty, IntegerProperty,
    UniqueIdProperty, DateProperty, RelationshipTo, Relationship, StructuredRel, IntegerProperty)
from pprint import pprint

class DiscordRelationship(StructuredRel):
  on_date = DateProperty(default_now = True)

class Guilds(StructuredNode):
  identifier  = StringProperty(unique_index=True, required=True)
  guild_name  = StringProperty(required=True)
  icon_url    = StringProperty(required=True)

class Channels(StructuredNode):
  identifier          = StringProperty(unique_index=True, required=True)
  channel_name        = StringProperty(required=True)
  channel_type        = StringProperty(required=True)
  category_id         = StringProperty(required=True)
  category            = StringProperty(required=True)
  guild_id            = RelationshipTo('Guilds', 'guild_channel')
  # discord_topic       = StringProperty(required=True)
  channel_name_length = StringProperty(required=True)

class Authors(StructuredNode):
  identifier       = StringProperty(unique_index=True, required=True)
  guild_id         = RelationshipTo('Guilds', 'author_guild')
  author_name      = StringProperty(required=True)
  nickname         = StringProperty(required=True)
  # color            = StringProperty(required=True)
  is_bot           = StringProperty(required=True)
  avatar_url       = StringProperty(required=True)

class Messages(StructuredNode):
  identifier           = StringProperty(unique_index=True, required=True)
  guild_id             = RelationshipTo('Guilds', 'message_guild')
  attachments          = StringProperty(required=True)
  author_guild_id      = RelationshipTo('Authors',   'message_author_id')
  channel_id           = RelationshipTo('Channels',  'message_channel')
  msg_content          = StringProperty(required=True)
  msg_content_length   = IntegerProperty(required=True)
  is_bot               = StringProperty(required=True)
  isPinned             = StringProperty(required=True)
  mentions             = StringProperty(required=True)
  msg_type             = StringProperty(required=True)
  msg_timestamp        = DateProperty(required=True)
  # msg_timestamp_edited = DateProperty(required=True)

class Attachments(StructuredNode):
  identifier       = StringProperty(unique_index=True, required=True)
  attachment_url      = StringProperty(required=True) 
  file_extension      = StringProperty(required=True) 
  file_size_bytes     = IntegerProperty(required=True) 
  message_id          = RelationshipTo('Messages',  'attachment_message') 
  author_guild_id     = RelationshipTo('Authors',   'attachment_author')
  guild_id            = RelationshipTo('Guilds',    'attachment_guild') 


class Emoji(StructuredNode):
  identifier         = StringProperty(unique_index=True, required=True)
  emoji_code         = StringProperty(required=True) 
  emoji_name         = StringProperty(required=True)
  emoji_json         = StringProperty(required=True)  


class Reactions(StructuredNode):
  identifier         = StringProperty(unique_index=True, required=True)
  message_id         = RelationshipTo('Messages', 'reaction_message') 
  author_guild_id    = RelationshipTo('Authors',  'reaction_author')
  channel_id         = RelationshipTo('Channels', 'reaction_channel')
  guild_id           = RelationshipTo('Guilds',   'reaction_guild') 
  reaction_count     = IntegerProperty(required=True) 
  emoji              = RelationshipTo('Emoji',   'reaction_emoji') 


class Replies(StructuredNode):
  identifier               = StringProperty(unique_index=True, required=True)
  guild_id                 = RelationshipTo('Guilds',   'reply_guild') 
  channel_id               = RelationshipTo('Channels', 'reply_channel')
  author_id                = StringProperty(required=True)
  author_guild_id          = RelationshipTo('Guilds',   'reply_author') 
  reply_to_channel_id      = RelationshipTo('Channels', 'reply_channel')
  reply_to_message_id      = RelationshipTo('Messages', 'reply_message') 
  reply_to_author_id       = StringProperty(required=True)
  reply_to_author_guild_id = RelationshipTo('Authors',  'reply_op')

class Mentions(StructuredNode):
  identifier         = StringProperty(unique_index=True, required=True)
  message_id         = RelationshipTo('Messages', 'mention_message') 
  author_guild_id    = RelationshipTo('Authors',  'mention_author')
  channel_id         = RelationshipTo('Channels', 'mention_channel')
  guild_id           = RelationshipTo('Guilds',   'mention_guild')


# config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'  # default
# db.set_connection()

# with db.transaction:
#   Guilds(identifier = "123", guild_name = "123", iconUrl = "123").save()