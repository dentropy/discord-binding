query_args = [i for i in range(1, 101)]
queries = [
  # {
  #   "name" : "Template",
  #   "desciption": "Template",
  #   "required_args": [],
  #   "arg_order" : [],
  #   "sql_query" : """
  #   """
  # },
  {
    "name" : "list_guilds",
    "desciption": "What are the discord guilds are in the database?",
    "required_args": [],
    "arg_order" : [],
    "sql_query" : """
      select
        id as guild_id,
        guild_name,
        guild_name as label
      from
        guilds_t;
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
        channel_name as label,
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
          authors_t.nickname as label,
          guilds_t.id as guild_id
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
    "name" : "guild_author_most_days_with_messages",
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
  },
  {
    "name" : "count_messages_per_channel_for_user_in_guild",
    "desciption": "How many messages has a user posted in each discord channel of a particular discord guild?",
    "uuid": "d4d9a29d-c144-4b7b-bb49-af768905cd79",
    "required_args": ["guild_id", "author_id"],
    "arg_order" : ["guild_id", "author_id", "author_id"],
    "sql_query" : """
        select
          author_channel_msg_count_t.channel_id,
          channels_t.channel_name,
          authors_t.author_name,
          authors_t.nickname,
          msg_count,
          guilds_t.guild_name,
          authors_t.id as authors_guild_id,
          guilds_t.id
        from
        (
          select
            count(*) as msg_count,
            channel_id
          from
            messages_t
          where
            guild_id = '{}'
            and author_guild_id = '{}'
          group by channel_id
        ) as author_channel_msg_count_t
      join channels_t on author_channel_msg_count_t.channel_id = channels_t.id
      join authors_t on '{}' = authors_t.id
      join guilds_t  on guilds_t.id = authors_t.guild_id
      order by msg_count desc;
    """
  },
  {
    "name" : "guild_author_most_reacted_messages",
    "desciption": "What discord messages were reacted to the most from this particular author?",
    "uuid": "f386a8f1-5a03-4800-b3fb-9ff569a064af",
    "required_args": ["guild_id", "author_id"],
    "arg_order" : ["guild_id", "author_id"],
    "sql_query" : """
      select 
        guilds_t.guild_name,
        channels_t.channel_name,
        authors_t.author_name,
        authors_t.nickname,
        reaciton_sum,
        messages_t.msg_content,
        guilds_t.id,
        channels_t.id,
        authors_t.id,
        messages_t.id as message_id
      from
      (
        select 
          sum(reaction_count) as reaciton_sum,
          message_id
        from 
        (
          select 
            author_messages_t.author_guild_id,
            message_id,
            msg_content,
            guild_id,
            channel_id,
            emoji_id,
            emoji_code,
            emoji_name,
            emoji_json,
            reaction_count
          from
            (
            select
              author_guild_id,
              id as messsage_id,
              msg_content
            from
              messages_t
            where
              guild_id = '{}'
              and author_guild_id = '{}'
            group by id, msg_content
            ) as author_messages_t
          join reactions_t on author_messages_t.messsage_id = reactions_t.message_id
        ) as messages_with_reactions_t
        group by message_id
      ) as msg_with_reaction_count_t
      join messages_t on msg_with_reaction_count_t.message_id = messages_t.id
      join channels_t on messages_t.channel_id = channels_t.id
      join authors_t on messages_t.author_guild_id = authors_t.id
      join guilds_t on messages_t.guild_id = guilds_t.id
      order by reaciton_sum desc;
    """
  },
  {
    "name" : "guild_author_messages_by_hour_of_day",
    "desciption": "What time of day does the particular discord author post their messages, group by hour?",
    "uuid": "d0faa6c6-be48-4170-941a-a30d833f6d1c",
    "required_args": ["guild_id", "author_id"],
    "arg_order" : ["guild_id", "author_id"],
    "sql_query" : """
      select
        guilds_t.guild_name,
        authors_t.author_name,
        authors_t.nickname,
        agg_days_posted_t.hour_of_day,
        num_messages_per_hour,
        guilds_t.id,
        agg_days_posted_t.author_guild_id
      from
      (
        select
          author_guild_id,
          day_message_t.hour_of_day,
          count(day_message_t.hour_of_day) as num_messages_per_hour
        from
        (
          select
            author_guild_id,
            extract(hour from msg_timestamp) hour_of_day
          from
            messages_t
          where
            guild_id = '{}'
            and author_guild_id = '{}'
        ) as day_message_t
        group by author_guild_id, day_message_t.hour_of_day
      ) as agg_days_posted_t
      join authors_t on authors_t.id = agg_days_posted_t.author_guild_id
      join guilds_t  on guilds_t.id  = authors_t.guild_id
      order by hour_of_day asc;
    """
  },
  {
    "name" : "guild_author_most_reaction_to_attachment",
    "desciption": "What message with an attachment from a particular author in a discord guild got the most reactions?",
    "uuid": "2c19f286-32de-4f5e-94f0-98d6eae21492",
    "required_args": ["guild_id", "author_id"],
    "arg_order" : ["guild_id", "author_id"],
    "sql_query" : """
      select 
        guilds_t.guild_name,
        channels_t.channel_name,
        authors_t.author_name,
        authors_t.nickname,
        reaciton_sum,
        messages_t.msg_content,
        guilds_t.id,
        channels_t.id,
        authors_t.id,
        messages_t.id as message_id
      from
      (
        select 
          sum(reaction_count) as reaciton_sum,
          message_id
        from 
        (
          select 
            author_messages_t.author_guild_id,
            message_id,
            channel_id,
            msg_content,
            guild_id,
            reaction_count
          from
            (
            select
              author_guild_id,
              id as messsage_id,
              msg_content
            from
              messages_t
            where
              guild_id = '{}'
              and author_guild_id = '{}'
            ) as author_messages_t
          join reactions_t on author_messages_t.messsage_id = reactions_t.message_id
        ) as messages_with_reactions_t
        group by message_id
      ) as msg_with_reaction_count_t
      join messages_t on msg_with_reaction_count_t.message_id = messages_t.id
      join channels_t on messages_t.channel_id = channels_t.id
      join authors_t on messages_t.author_guild_id = authors_t.id
      join guilds_t on messages_t.guild_id = guilds_t.id
      order by reaciton_sum desc;
    """
  },
  {
    "name" : "guild_author_messages_day_of_week",
    "desciption": "What day of the week does the particular discord author post their messages?",
    "uuid": "cb543a19-8513-43ae-8720-5ffeaec4a385",
    "required_args": ["guild_id", "author_id"],
    "arg_order" : ["guild_id", "author_id"],
    "sql_query" : """
      select
        guilds_t.guild_name,
        authors_t.author_name,
        authors_t.nickname,
        agg_days_posted_t.day_of_week,
        agg_days_posted_t.day_of_week_number,
        num_messages_on_day,
        guilds_t.id,
        agg_days_posted_t.author_guild_id
      from
      (
        select
          author_guild_id,
          day_message_t.day_of_week,
          day_message_t.day_of_week_number,
          count(day_message_t.day_of_week) as num_messages_on_day
        from
        (
          select
            author_guild_id,
            TO_CHAR(msg_timestamp, 'Day') as day_of_week,
            EXTRACT(DOW FROM msg_timestamp) AS day_of_week_number
          from
            messages_t
          where
              guild_id = '{}'
              and author_guild_id = '{}'
        ) as day_message_t
        group by author_guild_id, day_message_t.day_of_week, day_message_t.day_of_week_number
      ) as agg_days_posted_t
      join authors_t on authors_t.id = agg_days_posted_t.author_guild_id
      join guilds_t  on guilds_t.id  = authors_t.guild_id
      order by agg_days_posted_t.day_of_week_number asc;
    """
  },
  # {
  #   "name" : "guild_author_most_messages",
  #   "desciption": "What authors posted the most in a specific discord guild?",
  #   "uuid": "7922cc2d-f1cc-435d-832d-5fa4d555b121",
  #   "required_args": ["guild_id"],
  #   "arg_order" : ["guild_id"],
  #   "sql_query" : """
  #     select 
  #       guilds_t.guild_name,
  #       authors_t.author_name,
  #       author_msg_count.msg_count,
  #       author_msg_count.guild_id,
  #       authors_t.author_id as author_id,
  #       author_msg_count.author_guild_id
  #     from 
  #     (
  #       select 
  #         guild_id,
  #         author_guild_id,
  #         count(content) as msg_count
  #       from
  #         messages_t
  #       where 
  #         guild_id = '{}'
  #       group by
  #         guild_id,
  #         author_guild_id
  #     ) as author_msg_count
  #     join guilds_t on author_msg_count.guild_id = guilds_t.id
  #     join authors_t on author_msg_count.author_guild_id = authors_t.id
  #     order by msg_count desc;
  #   """
  # },
  {
    "name" : "guild_activity_per_month",
    "desciption": "How much activity for a specific discord guild per month?",
    "uuid": "efcd6f7d-b36e-4032-b89b-0fe9fd5a0da9",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select distinct guilds_t.id , guilds_t.guild_name, month_timestamp, msg_count from (
        select
          distinct DATE_TRUNC('month', msg_timestamp)
                    AS  month_timestamp,
            COUNT(guild_id) AS msg_count,
            guild_id 
        FROM messages_t
        WHERE guild_id = '{}'
        GROUP BY guild_id, month_timestamp
      ) as month_messages_t
      join guilds_t on month_messages_t.guild_id = guilds_t.id
      order by guilds_t.id, month_timestamp;
    """
  },
  {
    "name" : "guild_channels_most_active",
    "desciption": "What are the most active channels in a specific discord guild?",
    "uuid": "45f50e6a-fb81-4f7c-87b6-70785da72633",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select
        guilds_t.id as guild_id,
        guilds_t.guild_name ,
        channels_t.id,
        channels_t.channel_name,
        message_count
      from 
      (
        select 
          guild_id,
          channel_id,
          COUNT(id) as message_count
          from messages_t
        where 
          guild_id = '{}'
        group by guild_id, channel_id
      ) as messages_channel_agg_t
      join channels_t on messages_channel_agg_t.channel_id = channels_t.id
      join guilds_t on channels_t.guild_id = guilds_t.id
      order by message_count desc;
    """
  },
  {
    "name" : "guild_messages_percent_total_days",
    "desciption": "What percentage of days actually have messages for a specific discord guild?",
    "uuid": "3fb84a3c-742b-423a-a881-d5b46fd82a28",
    "required_args": ["guild_id"],
    "arg_order" : ["guild_id"],
    "sql_query" : """
      select 
        id,
        guild_name,
        min(day_timestamp)::DATE as earliest_date,
        max(day_timestamp)::DATE as latest_date,
        count(*) as days_with_messages,
          max(day_timestamp)::DATE - min(day_timestamp)::DATE as total_num_of_days,
          cast( count(*) as FLOAT) / cast( ( max(day_timestamp)::DATE - min(day_timestamp)::DATE ) as Float)* 100 as percentage_of_days
      from
      (
        select 
          distinct 
            guilds_t.id,
            guilds_t.guild_name,
            day_timestamp,
            msg_count 
        from (
          select distinct
            DATE_TRUNC('day', msg_timestamp) AS  day_timestamp,
              COUNT(guild_id) AS msg_count,
              guild_id 
          FROM messages_t
          WHERE
            messages_t.guild_id = '{}'
          GROUP BY guild_id, day_timestamp
        ) as month_messages_t
        join guilds_t on month_messages_t.guild_id = guilds_t.id
        order by day_timestamp desc
      ) as daily_msg_stats_t
      group by id, guild_name;
    """
  },
  
]