from neomodel import (config, db, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, DateProperty, RelationshipTo, Relationship, StructuredRel, IntegerProperty)
from pprint import pprint

class DiscordRelationship(StructuredRel):
    on_date = DateProperty(default_now = True)

class Guilds(StructuredNode):
    identifier  = StringProperty(unique_index=True, required=True)
    guild_name  = StringProperty(required=True)
    iconUrl     = StringProperty(required=True)

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
  author_id        = StringProperty(unique_index=True)
  guild_id         = RelationshipTo('Guilds', 'author_guild')
  author_name      = StringProperty(required=True)
  nickname         = StringProperty(required=True)
  # color            = StringProperty(required=True)
  isBot            = StringProperty(required=True)
  avatarUrl        = StringProperty(required=True)

class Messages(StructuredNode):
  identifier           = StringProperty(unique_index=True, required=True)
  guild_id             = RelationshipTo('Guilds', 'message_guild')
  attachments          = StringProperty(required=True)
  # author_id            = RelationshipTo('Authors',  'message_author')
  author_guild_id      = RelationshipTo('Authors',   'message_author_id')
  channel_id           = RelationshipTo('Channels',  'message_channel')
  content              = StringProperty(required=True)
  content_length       = IntegerProperty(required=True)
  isBot                = StringProperty(required=True)
  isPinned             = StringProperty(required=True)
  mentions             = StringProperty(required=True)
  msg_type             = StringProperty(required=True)
  msg_timestamp        = DateProperty(required=True)
  # msg_timestamp_edited = DateProperty(required=True)


# config.AUTO_INSTALL_LABELS = True
# config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'  # default
# db.set_connection()

# with db.transaction:
#   Guilds(identifier = "123", guild_name = "123", iconUrl = "123").save()