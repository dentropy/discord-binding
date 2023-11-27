query_args = [i for i in range(1, 101)]
queries = [
  {
    "name" : "Template",
    "desciption": "Template",
    "required_args": [],
    "arg_order" : [],
    "sql_query" : """
    """
  },
  {
    "name" : "list_guilds",
    "desciption": "What are the discord guilds are in the database?",
    "required_args": [],
    "arg_order" : [],
    "sql_query" : """
      select id as guild_id, guild_name from guilds_t;
    """
  },
  {
    "name" : "guild_channels",
    "desciption": "What are the channels of a particular discord guild?",
    "required_args": ["guild_id"],
    "arg_order" : [ "guild_id" ],
    "sql_query" : """
      select
        distinct(channels_t.id) as channel_id,
        guilds_t.guild_name,
        channel_name,
        guilds_t.id as guild_id
      from
        channels_t
      join guilds_t on channels_t.guild_id = guilds_t.id
      where
      guild_id in (  '{}'  );
      """
  },
  {
    "name" : "guild_authors",
    "desciption": "What authors posted in a particular discord guild?",
    "required_args": ["guild_id"],
    "arg_order" : [ "guild_id" ],
    "sql_query" : """
        select
          distinct(authors_t.id) as author_guild_id,
          authors_t.author_name,
          authors_t.author_name,
          authors_t.nickname,
          authors_t.id as guild_id
        from
          authors_t
        join guilds_t on authors_t.guild_id = guilds_t.id
        where
        guild_id in (  '{}'  );
      """
  },
  {
    "name" : "channel_authors",
    "desciption": "What authors posted in a specific discord channel?",
    "required_args": ["channel_id"],
    "arg_order" : [ "channel_id" ],
    "sql_query" : """
        select
          distinct(authors_t.id) as author_guild_id,
          authors_t.author_name,
          authors_t.author_name,
          authors_t.nickname,
          authors_t.guild_id
        from
          messages_t
        join authors_t on messages_t.author_guild_id = authors_t.id
        where
        channel_id in (  '{}' );
      """
  },
  {
    "name" : "channel_messages",
    "desciption": "What messages were posted in a discord channel with an offset?",
    "required_args": ["channel_id", "order", "offset"],
    "arg_order" : ["channel_id", "order", "offset"],
    "sql_query" : """
      select
        id as msg_id,
        guild_id,
        msg_content,
        msg_timestamp,
        msg_timestamp_edited,
        reply_to_message_id
      from
        messages_t
      where
        channel_id = '{}'
      order by msg_timestamp {}
      limit 1000
      offset {}
      """
  }
]