from urllib.parse import urlparse
import psycopg2
import psycopg2.extras
from pprint import pprint
import pandas as pd
import os

class DiscordAnalytics():
    def __init__(
        self,
        db_url,
        guild_white_list = []
    ):
        self.db_url = db_url
        url = urlparse(db_url)
        self.con = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password
        )
        self.cur = self.con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        self.guild_white_list = guild_white_list
        self.month_df = pd.DataFrame()
    def fetch_all_guilds(self):
        query = """
            select
                distinct id as guild_id, guild_name
            from
                guilds_t;
        """
        self.cur.execute(query)
        guild_list = self.cur.fetchall()
        guild_list_df = pd.DataFrame(guild_list)
        return guild_list_df
    def set_guild_white_list(self, guild_white_list):
        self.guild_white_list = pd.DataFrame({ "guild_id" : guild_white_list })
        self.df = pd.DataFrame({ "guild_id" : guild_white_list })
        return ["guild_id"]
    def get_guild_names(self):
        column_name = "guild_name"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        query = """
            select 
                guild_name as guild_name
            from
                guilds_t
            where
                id = %s;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["guild_name"])
        self.df[column_name] = result_list
        return [column_name]
    def earliest_message_per_guild(self):
        column_name = "earliest_message"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        query = """
            select 
                msg_timestamp
            from
                messages_t
            where
                guild_id = %s
            order by msg_timestamp asc
            limit 1;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["msg_timestamp"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_percentage_of_days_with_messages(self):
        column_name_list = ["earliest_date", "earliest_date", "latest_date", "num_days_with_messages", "total_days_with_messages", "percentage_of_days"]
        for column_name in column_name_list:
            if column_name in self.df:
                self.df.drop(column_name, axis=1)
        result_list = []
        query = """
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
            		WHERE messages_t.guild_id = %s
            		GROUP BY guild_id, day_timestamp
            	) as month_messages_t
            	join guilds_t on month_messages_t.guild_id = guilds_t.id
            	order by day_timestamp desc
            ) as daily_msg_stats_t
            group by id, guild_name;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append({
                "guild_id" : query_result[0]["id"],
                "earliest_date" : query_result[0]["earliest_date"],
                "latest_date" : query_result[0]["latest_date"],
                "num_days_with_messages" : query_result[0]["days_with_messages"],
                "total_days_with_messages" : query_result[0]["total_num_of_days"],
                "percentage_of_days" : query_result[0]["percentage_of_days"]
            })
        tmp_df = pd.DataFrame(result_list)
        self.df = self.df.merge(tmp_df, on='guild_id', how='inner')
        return column_name_list
    def calculate_num_authors_per_guild(self):
        column_name = "author_account"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        query = """
            select
                count(*) as count
            from
                authors_t
            where
                isBot = 'False'
                and guild_id = %s;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_num_bot_authors_per_guild(self):
        column_name = "bot_author_count"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        query = """
            select
                count(*) as count
            from
                authors_t
            where
                isBot = 'True'
                and guild_id = %s;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_num_channels_per_guild(self):
        column_name = "channel_count"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        query = """
            select 
                count( distinct id) as count
            from
                channels_t
            where
                guild_id = %s;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_num_messages_per_guild(self):
        column_name = "message_count"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        query = """
            select 
                count( distinct id) as count
            from
                messages_t
            where
                isBot = 'F'
                and guild_id = %s;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculte_num_bot_messages_per_guild(self):
        column_name = "bot_message_count"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        query = """
            select 
                count( distinct id) as count
            from
                messages_t
            where
                isBot = 'T'
                and guild_id = %s;
            """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_num_authors_more_x_messages(self, x):
        column_name = f"num_authors_more_{str(x)}_messages"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        for guild_id in self.df["guild_id"]:
            query = """
            select 
            	guild_message_count_t.guild_id as guild_id,
            	count(*) as count
            from 
            (
            	select * FROM
            		(
            			select 
            				guild_id,
            				author_id,
            				count(content) as msg_count
            			from messages_t
            			group by guild_id, author_id
            		) as raw_author_message_count
            	where 
                    msg_count > %s
                    and guild_id = %s
            ) as guild_message_count_t
            group by guild_message_count_t.guild_id
            """
            self.cur.execute(query, [str(x), str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_num_authors_less_x_messages(self, x):
        column_name = f"num_authors_less_{str(x)}_messages"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        for guild_id in self.df["guild_id"]:
            query = """
            select 
            	guild_message_count_t.guild_id as guild_id,
            	count(*) as count
            from 
            (
            	select * FROM
            		(
            			select 
            				guild_id,
            				author_id,
            				count(content) as msg_count
            			from messages_t
            			group by guild_id, author_id
            		) as raw_author_message_count
            	where 
                    msg_count < %s
                    and guild_id = %s
            ) as guild_message_count_t
            group by guild_message_count_t.guild_id
            """
            self.cur.execute(query, [str(x), str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [ column_name ]
    def calculate_num_authors_between_msg_count(self, x, y):
        column_name = f"num_authors_between_msg_count_{str(x)}_and_{str(y)}"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        for guild_id in self.df["guild_id"]:
            query = """
            select 
            	guild_message_count_t.guild_id as guild_id,
            	count(*) as count
            from 
            (
            	select * FROM
            		(
            			select 
            				guild_id,
            				author_id,
            				count(content) as msg_count
            			from messages_t
            			group by guild_id, author_id
            		) as raw_author_message_count
            	where 
                    msg_count > %s
                    and msg_count < %s
                    and guild_id = %s
            ) as guild_message_count_t
            group by guild_message_count_t.guild_id
            """
            self.cur.execute(query, [str(x), str(y), str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_average_message_count_for_most_active_x_days(self, x, y):
        column_name = f"num_authors_between_msg_count_{str(x)}_and_{str(y)}"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        for guild_id in self.df["guild_id"]:
            query = """
            select 
            	guild_message_count_t.guild_id as guild_id,
            	count(*) as count
            from 
            (
            	select * FROM
            		(
            			select 
            				guild_id,
            				author_id,
            				count(content) as msg_count
            			from messages_t
            			group by guild_id, author_id
            		) as raw_author_message_count
            	where 
                    msg_count < %s
                    and msg_count > %s
                    and guild_id = %s
            ) as guild_message_count_t
            group by guild_message_count_t.guild_id
            """
            self.cur.execute(query, [str(x), str(y), str(guild_id), ])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_average_half_life_top_x_percent_users(self, x, min_msg_length):
        column_name = f"average_half_life_top_{x}_percent_users_min_message_count_{min_msg_length}"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        query = """
            SELECT 
                guilds_t.guild_name,
                guilds_t.id,
                EXTRACT(DAY FROM average_author_half_life) as average_author_half_life,
                average_author_half_life as average_author_half_life_timestamp
            from
            (
                select 
                    guild_id,
                    avg(author_half_life) as average_author_half_life
                from
                (
                    select 
                        guild_message_count_t.guild_id as guild_id,
                        guilds_t.guild_name,
                        msg_count,
                        max_msg_timestamp,
                        min_msg_timestamp,
                        max_msg_timestamp - min_msg_timestamp as author_half_life
                    from 
                    (
                        select * FROM
                            (
                                select 
                                    guild_id,
                                    author_id,
                                    count(content) as msg_count,
                                    max(msg_timestamp) as max_msg_timestamp,
                                    min(msg_timestamp) as min_msg_timestamp
                                from messages_t
                                group by guild_id, author_id
                            ) as msg_something_t
                        where msg_count > %s -- min_message_length
                        and guild_id = %s
                    ) as guild_message_count_t
                    join guilds_t on guild_message_count_t.guild_id = guilds_t.id
                    order by author_half_life desc
                    limit (
                        select cast(  cast(author_count as float) / 100 * %s as Integer) -- Percentage
                            as percentage_msg_count
                        from 
                        (
                            select guild_id, COUNT(*) as author_count FROM
                                (
                                    select 
                                        guild_id,
                                        author_id,
                                        count(content) as msg_count
                                    from messages_t
                                    group by guild_id, author_id
                                ) as msg_something_t
                            where msg_count > 2 -- min_message_length
                            and guild_id = %s
                            group by guild_id
                        ) as author_count_t
                    )
                )  as avg_halflife_percentage_author_t
                group by guild_id
            ) as average_author_half_list
            join guilds_t on guilds_t.id = average_author_half_list.guild_id
        """
        result_list = []
        result_list_2 = []
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [str(min_msg_length), guild_id, str(x), guild_id])
            query_result = self.cur.fetchall()
            if query_result == []:
                return False
            result_list.append(query_result[0]["average_author_half_life"])
            result_list_2.append(query_result[0]["average_author_half_life_timestamp"])
        self.df[column_name ] = result_list
        self.df[column_name + "_timestamp"] = result_list_2
        return [column_name, column_name + "_timestamp"]
    def calculate_base_guild_stats(self):
        self.get_guild_names()
        self.calculate_num_authors_per_guild()
        self.calculate_num_bot_authors_per_guild()
        self.calculate_num_channels_per_guild()
        self.calculate_num_messages_per_guild()
        self.calculte_num_bot_messages_per_guild()
        self.earliest_message_per_guild()
    def calculate_monthly_author_messages(self):
        if "latest_date" not in self.df or "earliest_date" not in self.df:
            self.calculate_percentage_of_days_with_messages()
        df_to_join = pd.DataFrame()
        query = """
        select distinct guilds_t.id as guild_id, guilds_t.guild_name, month_timestamp, msg_count as msg_count_per_month from (
        	select
        		distinct DATE_TRUNC('month', msg_timestamp)
        			         AS  month_timestamp,
        	    COUNT(guild_id) AS msg_count,
        	    guild_id 
        	FROM messages_t
            WHERE 
                messages_t.guild_id = %s
                and isBot = 'F'
        	GROUP BY guild_id, month_timestamp
        ) as month_messages_t
        join guilds_t on month_messages_t.guild_id = guilds_t.id
        order by guilds_t.id, month_timestamp;
        """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [guild_id])
            query_result = self.cur.fetchall()
            tmp_df = pd.DataFrame(query_result)
            df_to_join = pd.concat([df_to_join, tmp_df])
        if len(self.month_df) == 0:
            self.month_df = df_to_join
        else:
            self.month_df = pd.merge(self.month_df, df_to_join, on=['guild_id','month_timestamp', 'guild_name'], how='outer')
        return ['guild_id', 'guild_name', 'month_timestamp', 'msg_count_per_month']
    def calculate_monthly_bot_messages(self):
        if "latest_date" not in self.df or "earliest_date" not in self.df:
            self.calculate_percentage_of_days_with_messages()
        df_to_join = pd.DataFrame()
        query = """
        select distinct guilds_t.id as guild_id, guilds_t.guild_name, month_timestamp, msg_count as bot_msg_count_per_month from (
        	select
        		distinct DATE_TRUNC('month', msg_timestamp)
        			         AS  month_timestamp,
        	    COUNT(guild_id) AS msg_count,
        	    guild_id 
        	FROM messages_t
            WHERE 
                messages_t.guild_id = %s
                and isBot = 'T'
        	GROUP BY guild_id, month_timestamp
        ) as month_messages_t
        join guilds_t on month_messages_t.guild_id = guilds_t.id
        order by guilds_t.id, month_timestamp;
        """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [guild_id])
            query_result = self.cur.fetchall()
            tmp_df = pd.DataFrame(query_result)
            df_to_join = pd.concat([df_to_join, tmp_df])
        if len(self.month_df) == 0:
            self.month_df = df_to_join
        else:
            self.month_df = pd.merge(self.month_df, df_to_join, on=['guild_id','month_timestamp', 'guild_name'], how='outer')
        return ['guild_id', 'guild_name', 'month_timestamp', 'bot_msg_count_per_month']
    def calculate_monthly_active_authors(self):
        if "latest_date" not in self.df or "earliest_date" not in self.df:
            self.calculate_percentage_of_days_with_messages()
        df_to_join = pd.DataFrame()
        query = """
            select 
            	distinct 
            	guilds_t.id as guild_id, 
            	guilds_t.guild_name, 
            	month_timestamp, 
            	author_count as author_count_per_month
            from 
            (
            	select
            		distinct DATE_TRUNC('month', msg_timestamp) AS  month_timestamp,
            	    COUNT( distinct author_id) AS author_count,
            	    guild_id 
            	FROM messages_t
                WHERE 
                    guild_id = %s
                    and isBot = 'F'
            	GROUP BY guild_id, month_timestamp
            ) as month_messages_t
            join guilds_t on month_messages_t.guild_id = guilds_t.id
            order by guilds_t.id, month_timestamp;
        """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [guild_id])
            query_result = self.cur.fetchall()
            tmp_df = pd.DataFrame(query_result)
            df_to_join = pd.concat([df_to_join, tmp_df])
        if len(self.month_df) == 0:
            self.month_df = df_to_join
        else:
            self.month_df = pd.merge(self.month_df, df_to_join, on=['guild_id','month_timestamp', 'guild_name'], how='outer')
        return ['guild_id', 'guild_name', 'month_timestamp', 'author_count_per_month']
    def calculate_monthly_active_bots(self):
        if "latest_date" not in self.df or "earliest_date" not in self.df:
            self.calculate_percentage_of_days_with_messages()
        df_to_join = pd.DataFrame()
        query = """
            select 
            	distinct 
            	guilds_t.id as guild_id, 
            	guilds_t.guild_name, 
            	month_timestamp, 
            	author_count as bot_count_per_month
            from 
            (
            	select
            		distinct DATE_TRUNC('month', msg_timestamp) AS  month_timestamp,
            	    COUNT( distinct author_id) AS author_count,
            	    guild_id 
            	FROM messages_t
                WHERE 
                    guild_id = %s
                    and isBot = 'T'
            	GROUP BY guild_id, month_timestamp
            ) as month_messages_t
            join guilds_t on month_messages_t.guild_id = guilds_t.id
            order by guilds_t.id, month_timestamp;
        """
        for guild_id in self.df["guild_id"]:
            self.cur.execute(query, [guild_id])
            query_result = self.cur.fetchall()
            tmp_df = pd.DataFrame(query_result)
            df_to_join = pd.concat([df_to_join, tmp_df])
        if len(self.month_df) == 0:
            self.month_df = df_to_join
        else:
            self.month_df = pd.merge(self.month_df, df_to_join, on=['guild_id','month_timestamp', 'guild_name'], how='outer')
        return ['guild_id', 'guild_name', 'month_timestamp', 'bot_count_per_month']
    def normalize_data(self, column_output_name, df, label, value):
        df[column_output_name] = df.groupby(label)[value].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        return df
    def calculate_normalized_month_df_column(self, column_input_name):
        self.month_df = self.normalize_data(column_input_name + "_normalized", self.month_df, 'guild_id', column_input_name )
        return [column_input_name + "_normalized"]
    def calculate_base_guild_stats(self):
        self.get_guild_names()
        self.calculate_num_authors_per_guild()
        self.calculate_num_bot_authors_per_guild()
        self.calculate_num_channels_per_guild()
        self.calculate_num_messages_per_guild()
        self.calculte_num_bot_messages_per_guild()
        self.earliest_message_per_guild()
        return self.df
    def calulate_demo_guild_stats(self):
        self.calculate_num_authors_more_x_messages(20)
        self.calculate_num_authors_less_x_messages(20)
        self.calculate_num_authors_between_msg_count(2,100)
        self.calculate_average_half_life_top_x_percent_users(20, 2)
        self.calculate_average_half_life_top_x_percent_users(30, 2)
        return self.df
    def caultate_monthly_guild_stats(self):
        self.calculate_monthly_author_messages()
        self.calculate_monthly_bot_messages()
        self.calculate_monthly_active_authors()
        self.calculate_monthly_active_bots()
        self.calculate_normalized_month_df_column("msg_count_per_month")
        self.calculate_normalized_month_df_column("bot_msg_count_per_month")
        self.calculate_normalized_month_df_column("author_count_per_month")
        self.calculate_normalized_month_df_column("bot_count_per_month")
        return self.month_df
    def concat_month_df_with_base_df(self):
        return pd.merge(self.month_df, self.df, on=['guild_id','guild_name'], how='outer')