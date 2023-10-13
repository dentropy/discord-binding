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
            print(column_name)
            print(query_result)
            if query_result == []:
                return False
            result_list.append(query_result[0]["msg_timestamp"])
        self.df[column_name] = result_list
        return [column_name]
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
            print(query_result)
            result_list.append(query_result[0]["count"])
        self.df[column_name] = result_list
        return [column_name]
    def calculate_average_half_life_top_x_percent_users(self, x, min_msg_length):
        column_name = f"average_half_life_top_{x}_percent_users_min_message_count_{min_msg_length}"
        if column_name in self.df:
            self.df.drop(column_name, axis=1)
        result_list = []
        result_list_2 = []
        for guild_id in self.df["guild_id"]:
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
    