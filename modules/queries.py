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
    "arg_order" : ["channel_id", "order", "offset", "order"],
    "sql_query" : """
      select 
        just_messages_t.msg_id,
        just_messages_t.guild_id,
        just_messages_t.msg_content,
        authors_t.author_name,
        authors_t.nickname,
        authors_t.author_id,
        just_messages_t.author_guild_id,
        just_messages_t.msg_timestamp,
        just_messages_t.msg_timestamp_edited,
        just_messages_t.reply_to_message_id
      from
      (
        select
              id as msg_id,
              guild_id,
              msg_content,
              author_guild_id,
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
      ) as just_messages_t
      join authors_t on authors_t.id = just_messages_t.author_guild_id
      order by msg_timestamp {};
      """
  },
  {
    "name" : "user_longest_avg_msg_length",
    "desciption": "What discord user has the longest average message length in a particular guild?",
    "uuid": "2f4fd09e-24a3-4359-81b2-049742a03610",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select 
        authors_t.author_name,
        authors_t.nickname,
        avg_content_length_t.content_length,
        avg_content_length_t.content_count,
        authors_t.id
      from 
      (
        select 
          author_guild_id, 
          count(msg_content_length) as content_count,
          AVG(msg_content_length) as content_length
        from
          messages_t
        where
          is_bot = false
          and guild_id in (  '{}'  )
        group by author_guild_id
      ) as avg_content_length_t
      join authors_t
      on authors_t.id = avg_content_length_t.author_guild_id
      order by avg_content_length_t.content_length desc;
      """
  },
  {
    "name" : "guild_author_most_messages",
    "desciption": "What discord user sent the most messages in a particular discord guild?",
    "uuid": "d473e743-c32d-45f7-bfe8-9836eeff97f4",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select
        authors_t.author_name,
        authors_t.nickname,
        msg_count_per_author_t.msg_count,
        msg_count_per_author_t.author_guild_id,
        guilds_t.guild_name,
        guilds_t.id as guild_id
      from
      (
        select
          count(*) as msg_count,
          author_guild_id
        from
          messages_t
        where 
          guild_id in (  '{}'  )
        group by author_guild_id
        order by msg_count desc
      ) as msg_count_per_author_t
      join authors_t on msg_count_per_author_t.author_guild_id = authors_t.id
      join guilds_t  on authors_t.guild_id = guilds_t.id
      order by msg_count_per_author_t.msg_count desc;
      """
  },
  {
    "name" : "guild_author_consistent",
    "desciption": "Who is the most consistent poster within a Discord Guild?",
    "uuid": "dba668aa-bb99-46d5-9942-9f41bed27766",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select
        authors_t.author_name,
        authors_t.nickname,
        count_msg_day_t.day_count,
        count_msg_day_t.author_guild_id,
        guilds_t.guild_name,
        guilds_t.id as guild_id
      from
      (
        select
          count(distinct_msg_day_t.num_days_posted) as day_count,
          distinct_msg_day_t.author_guild_id
        from 
        (
          SELECT 
            distinct ( TO_CHAR(msg_timestamp, 'YYYY-MM-DD') )
                as num_days_posted,
            author_guild_id
          from
            messages_t
          where guild_id = '{}'
        ) as distinct_msg_day_t
        group by distinct_msg_day_t.author_guild_id
        order by distinct_msg_day_t.author_guild_id desc
      ) as count_msg_day_t
      join authors_t on count_msg_day_t.author_guild_id = authors_t.id
      join guilds_t on authors_t.guild_id = guilds_t.id 
      order by day_count desc;
      """
  },
  {
    "name" : "guild_author_most_reactions",
    "desciption": "What discord author got the most reactions to their messages?",
    "uuid": "31ea5eb0-424d-4bac-ac87-dcc463b5d92d",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select
        authors_t.author_name,
        authors_t.nickname, 
        reaction_count_t.reaction_count,
        guilds_t.guild_name,
        reaction_count_t.author_guild_id,
        guilds_t.id as guild_id
      from
      (
        select 
          author_guild_id,
          sum(reaction_count) as reaction_count
        from
          reactions_t
        where
          guild_id = '{}'
        group by author_guild_id
      ) as reaction_count_t
      join authors_t on reaction_count_t.author_guild_id = authors_t.id
      join guilds_t  on authors_t.guild_id = guilds_t.id
      order by reaction_count desc;
      """
  },
  {
    "name" : "guild_author_distinct_reaction_count",
    "desciption": "What discord author got the most distinct reactions to their messages?",
    "uuid": "1045dbd7-8a3e-4975-8dea-fe81c3c354d1",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select
        authors_t.author_name,
        authors_t.nickname, 
        reaction_count_t.reaction_count,
        guilds_t.guild_name,
        reaction_count_t.author_guild_id,
        guilds_t.id as guild_id
      from
      (
        select 
          author_guild_id,
          count(distinct(reaction_count)) as reaction_count
        from
          reactions_t
        where
          guild_id in (  '{}'  )
        group by author_guild_id
      ) as reaction_count_t
      join authors_t on reaction_count_t.author_guild_id = authors_t.id
      join guilds_t  on authors_t.guild_id = guilds_t.id
      order by reaction_count desc;
    """
  },
  {
    "name" : "guild_author_most_messages_single_day",
    "desciption": "What discord user has the highest spike in activity in single day?",
    "uuid": "0c868cc8-6f4b-4f8c-9f50-ef2e1bf31615",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select 
        authors_t.author_name,
        authors_t.nickname,
        msg_date_agg_t.day_msg_count,
        msg_date_agg_t.author_guild_id,
        guilds_t.guild_name,
        guilds_t.id as guild_id
      from
      (
        select
          count(msg_date_t.msg_date) as day_msg_count,
          msg_date_t.msg_date,
          msg_date_t.author_guild_id
        from
        (
          SELECT
            TO_CHAR(msg_timestamp, 'YYYY-MM-DD') as msg_date,
            author_guild_id
          from
            messages_t
          where guild_id = '{}'
        ) as msg_date_t
        group by msg_date_t.msg_date, msg_date_t.author_guild_id
      ) as msg_date_agg_t
      join authors_t on msg_date_agg_t.author_guild_id = authors_t.id
      join guilds_t on authors_t.guild_id = guilds_t.id
      order by day_msg_count desc;
    """
  },
  {
    "name" : "guild_author_most_attachments",
    "desciption": "Who sent the most attachments in a specific discord guild?",
    "uuid": "bb1fc99d-24cc-4ea2-9110-3bf7d695ac03",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select
        authors_t.author_name,
        authors_t.nickname,
        attachment_msg_count_t.attachment_msg_count,
        guilds_t.guild_name,
        attachment_msg_count_t.author_guild_id,
        guilds_t.id as guild_id
      from
      (
        select 
          count(*) attachment_msg_count,
          author_guild_id
        from attachments_t
        where guild_id in (  '{}'  )
        group by author_guild_id
      ) as attachment_msg_count_t
      join authors_t on attachment_msg_count_t.author_guild_id = authors_t.id
      join guilds_t  on authors_t.guild_id = guilds_t.id
      order by attachment_msg_count_t.attachment_msg_count desc;
    """
  },
  {
    "name" : "guild_author_edit_percentage",
    "desciption": "What discord author edits the highest percentage of their messages within a particular discord guild?",
    "uuid": "80a2d7fc-3d80-420a-ba6b-d9bd41206606",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id", "guild_id"],
    "sql_query" : """
      select
        authors_t.author_name,
        authors_t.nickname,
        msg_timestamp_edited_count_t.msg_timestamp_edited_count,
        author_msg_count_t.msg_count,
        msg_timestamp_edited_count_t.msg_timestamp_edited_count::FLOAT  / author_msg_count_t.msg_count::FLOAT  * 100 as msg_edited_percentage,
        msg_timestamp_edited_count_t.author_guild_id,
        guilds_t.guild_name,
        guilds_t.id as guild_id
      from
      (
        select 
          count(*) as msg_timestamp_edited_count,
          author_guild_id
        from 
          messages_t
        where
          msg_timestamp_edited is not null
          and guild_id = '{}'
        group by author_guild_id
      ) as msg_timestamp_edited_count_t
      join (
        select 
          count(*) as msg_count,
          author_guild_id
        from 
          messages_t
          where guild_id = '{}'
        group by author_guild_id
      ) as author_msg_count_t on author_msg_count_t.author_guild_id = msg_timestamp_edited_count_t.author_guild_id
      join authors_t on msg_timestamp_edited_count_t.author_guild_id = authors_t.id
      join guilds_t  on authors_t.guild_id = guilds_t.id
      where msg_count > 1
      order by msg_edited_percentage desc;
    """
  },
  {
    "name" : "guild_author_most_question_messages",
    "desciption": "What discord user asked the most questions in a specific guild?",
    "uuid": "c102ef60-4b8c-423e-8102-69578c1ec330",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select 
        authors_t.author_name,
        authors_t.nickname,
        avg_content_length_t.content_length,
        avg_content_length_t.content_count,
        authors_t.id
      from 
      (
        select 
          author_guild_id, 
          count(msg_content_length) as content_count,
          AVG(msg_content_length) as content_length
        from
          messages_t
        where
          is_bot = false
          and guild_id = '{}'
          and msg_content like '%?%'
        group by author_guild_id
      ) as avg_content_length_t
      join authors_t
      on authors_t.id = avg_content_length_t.author_guild_id
      order by avg_content_length_t.content_count desc;
    """
  }

]