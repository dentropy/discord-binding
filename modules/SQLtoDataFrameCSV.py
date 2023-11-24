import os
from pprint import pprint
from decouple import AutoConfig
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
config = AutoConfig(search_path=current_directory)

import sys
sys.path.append(os.getcwd() + '/..')
from DiscordAnalytics import DiscordAnalytics

discord_analytics = DiscordAnalytics(config("db_url"))
import timeit

guilds_list = discord_analytics.fetch_all_guilds()
discord_analytics.set_guild_white_list(list(guilds_list["guild_id"].loc[0:]))

run_name = ""

print("calculate_table_row_counts")
discord_analytics.calculate_table_row_counts()
discord_analytics.table_size_df.to_csv(f"{run_name}table_size_df.csv")

print("calculate_base_guild_stats")
discord_analytics.calculate_base_guild_stats()
discord_analytics.calulate_demo_guild_stats()
discord_analytics.df.to_csv(f"{run_name}df.csv")

print("calculate_base_guild_stats")
discord_analytics.df.to_csv(f"./{run_name}full_df.csv")
discord_analytics.calulate_demo_guild_stats()

print("caultate_monthly_guild_stats")
discord_analytics.caultate_monthly_guild_stats()
discord_analytics.month_df.to_csv(f"./{run_name}month_df.csv")
print("Saving query_time_df")
discord_analytics.query_time_df.to_csv(f"./{run_name}query_time_df.csv")
print("Done")