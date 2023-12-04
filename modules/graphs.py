import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

from pprint import pprint
import pandas as pd

from modules.query_resolver import query_resolver
from modules.queries import queries

graph_names = {
    "user_longest_avg_msg_length" : {
        "query_name" : "user_longest_avg_msg_length"
    },
    "guild_author_most_messages" : {
        "query_name" : "guild_author_most_messages"
    },
    "guild_author_most_days_with_messages" : {
        "query_name" : "guild_author_most_days_with_messages"
    },
    "guild_author_most_reactions" : {
        "query_name" : "guild_author_most_reactions"
    },
    "guild_author_distinct_reaction_count" : {
        "query_name" : "guild_author_distinct_reaction_count"
    },
    "guild_author_most_messages_single_day" : {
        "query_name" : "guild_author_most_messages_single_day"
    },
    "guild_author_most_attachments" : {
        "query_name" : "guild_author_most_attachments"
    },
    "guild_author_edit_percentage" : {
        "query_name" : "guild_author_edit_percentage"
    },
    "count_messages_per_channel_for_user_in_guild" : {
        "query_name" : "count_messages_per_channel_for_user_in_guild"
    },
    "guild_author_most_reacted_messages" : {
        "query_name" : "guild_author_most_reacted_messages"
    },
    "guild_author_messages_by_hour_of_day" : {
        "query_name" : "guild_author_messages_by_hour_of_day"
    },
    "guild_author_messages_day_of_week" : {
        "query_name" : "guild_author_messages_day_of_week"
    },
    "guild_activity_per_month" : {
        "query_name" : "guild_activity_per_month"
    },
    "guild_message_per_channel" : {
        "query_name" : "guild_message_per_channel"
    },
    
    "guild_author_message_min_100" : {
        "query_name" : "guild_author_message_min_100"
    },
    "guild_channel_message_length" : {
        "query_name" : "guild_channel_message_length"
    },
    "guild_attachment_file_type_count" : {
        "query_name" : "guild_attachment_file_type_count"
    },
    "guild_channel_message_length" : {
        "query_name" : "guild_channel_message_length"
    },
    "guild_messages_month" : {
        "query_name" : "guild_messages_month"
    },
    "guild_activity_per_day_of_week" : {
        "query_name" : "guild_activity_per_day_of_week"
    },
    # "guild_activity_per_day_of_week" : {
    #     "query_name" : "guild_activity_per_day_of_week"
    # },
    "guild_domain_count" : {
        "query_name" : "guild_domain_count"
    },
    "guild_channel_author_count" : {
        "query_name" : "guild_channel_author_count"
    },
    "guild_author_mention_count" : {
        "query_name" : "guild_author_mention_count"
    },
    "guild_author_most_question_messages" : {
        "query_name" : "guild_author_most_question_messages"
    }
}

def list_graphs(queries):
    resturn_graphs = []
    for graph_name in graph_names.keys():
        pprint(graph_name)
        for query in queries:
            if query["name"] == graph_names[graph_name]["query_name"]:
                graph_names[graph_name]["query_data"] = query
                graph_names[graph_name]["label"] = query["desciption"]
                resturn_graphs.append(graph_names[graph_name])
    return resturn_graphs


def build_graph(pg_cursor, graph_name, query_args_dict):
    if graph_name not in graph_names.keys():
        return f"Error: {graph_name} is not in graph_names \n {graph_names}"
    if graph_name == "user_longest_avg_msg_length":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print("\nresult_df for user_longest_avg_msg_length\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : "user_longest_avg_msg_length",
            "desciption": "What discord user has the longest average message length in a particular guild?",
            "uuid": "2f4fd09e-24a3-4359-81b2-049742a03610",
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Average Content Length',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["content_length"], 
                        offsetgroup=1, 
                        orientation='v'
                    ),
                    go.Bar(
                        name='Content Count',  
                        x=result_df["nickname"], 
                        yaxis='y2', 
                        y = result_df["content_count"],
                        offsetgroup=2, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Average Content Length'},
                    'yaxis2': {'title': 'Content Count', 'overlaying': 'y', 'side': 'right'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Longest Average Message Length',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_most_messages":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": "2f4fd09e-24a3-4359-81b2-049742a03610",
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Names',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Message Count'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Message Count per Author',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_most_days_with_messages":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": "2f4fd09e-24a3-4359-81b2-049742a03610",
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Names',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["day_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Day Count'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Most Days with Messages',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_most_reactions":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Names',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["reaction_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Reaction Count'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Authors with most Reactions',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_distinct_reaction_count":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Names',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["reaction_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Reaction Varity Count'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Authors with most Varity of Reactions',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_most_messages_single_day":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Names',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["day_msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Messages in single day'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Authors sorted by most messages in single day',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_most_attachments":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Names',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["attachment_msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Number of Messages with Attachments'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Authors sorted by most messages with Attachments',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_edit_percentage":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Average Content Length',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["msg_edited_percentage"], 
                        offsetgroup=1, 
                        orientation='v'
                    ),
                    go.Bar(
                        name='Content Count',  
                        x=result_df["nickname"], 
                        yaxis='y2', 
                        y = result_df["msg_count"],
                        offsetgroup=2, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Message Editted Percentage'},
                    'yaxis2': {'title': 'Total Message Count', 'overlaying': 'y', 'side': 'right'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Message Editted Percentage verses Total Message Count',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_most_reacted_messages":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Individual Message',     
                        x=result_df["message_id"], 
                        yaxis='y',
                        y = result_df["reaciton_sum"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Reactions to message posted by {result_df.iloc[0]["nickname"]}'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Reactions to Messages from {result_df.iloc[0]["nickname"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }    
    if graph_name == "count_messages_per_channel_for_user_in_guild":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Channel Name',     
                        x=result_df["channel_name"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages from {result_df.iloc[0]["nickname"]}'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Messages from {result_df.iloc[0]["nickname"]} Per Hour of Day',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }

    if graph_name == "guild_author_messages_by_hour_of_day":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Hour of Day',     
                        x=result_df["hour_of_day"], 
                        yaxis='y',
                        y = result_df["num_messages_per_hour"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages from {result_df.iloc[0]["nickname"]}'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Messages from {result_df.iloc[0]["nickname"]} Per Hour of Day',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_messages_day_of_week":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Day of Week',     
                        x=result_df["day_of_week"], 
                        yaxis='y',
                        y = result_df["num_messages_on_day"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages from {result_df.iloc[0]["nickname"]}'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Messages from {result_df.iloc[0]["nickname"]} Per Day of Week',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_activity_per_month" or graph_name == "guild_messages_month":
        if  graph_name == "guild_messages_month":
            graph_name = "guild_activity_per_month"
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Month and Year',     
                        x=result_df["month_timestamp"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Messages per month in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_channels_most_active":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Channel Name',     
                        x=result_df["channel_name"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Messages per Channel in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_message_per_channel":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Channel Name',     
                        x=result_df["channel_name"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Messages per Channel in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_message_min_100":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Nickname',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Authors with more than 100 messages in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_channel_message_length":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Average Content Length',     
                        x=result_df["channel_name"], 
                        yaxis='y',
                        y = result_df["msg_length"], 
                        offsetgroup=1, 
                        orientation='v'
                    ),
                    go.Bar(
                        name='Content Count',  
                        x=result_df["channel_name"], 
                        yaxis='y2', 
                        y = result_df["msg_count"],
                        offsetgroup=2, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Average Message Length'},
                    'yaxis2': {'title': 'Total Message Count', 'overlaying': 'y', 'side': 'right'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Average Message Length per Channel and Message Count Per Channel in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_attachment_file_type_count":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        # pprint(result_df)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='File Type',     
                        x=result_df["file_extension"], 
                        yaxis='y',
                        y = result_df["extension_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Popularity of Attachment File Types in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_activity_per_day":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        # pprint(result_df)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Month - Year',     
                        x=result_df["month_timestamp"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Message Per Day of Week in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_activity_per_day_of_week":
        # query_name = graph_names["graph_names"]["query_name"]
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        # pprint(result_df)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Month - Year',     
                        x=result_df["month_timestamp"], 
                        yaxis='y',
                        y = result_df["msg_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Message Per Day of Week in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_domain_count":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        # pprint(result_df)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Domain Name',     
                        x=result_df["netloc"], 
                        yaxis='y',
                        y = result_df["count_domain"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Messages'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Popularity of Domain Names in Messages',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_channel_author_count":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        # pprint(result_df)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Channel',     
                        x=result_df["channel_name"], 
                        yaxis='y',
                        y = result_df["author_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Distinct Authors'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Distinct Authors in Each Channel within Guild {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_mention_count":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        pprint(result_df)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : graph_name,
            "desciption": selected_query["desciption"],
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Author Nickname',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["mention_count"], 
                        offsetgroup=1, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': f'Number of Author Mentions'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title=f'Number of Times a Author is Mentioned in {result_df.iloc[0]["guild_name"]}',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
    if graph_name == "guild_author_most_question_messages":
        result_df = query_resolver(pg_cursor, queries, graph_name, query_args_dict)
        selected_query = { "name" : "placeholder"}
        for query in queries:
            if graph_name == query["name"]:
                selected_query = query
        # print("\n\nselected_query")
        # pprint(selected_query)
        # print("\n\nquery_args_dict\n\n")
        # pprint(query_args_dict)
        # print(f"\nresult_df for graph_name\n\n")
        # pprint(result_df)
        # print("\nqueries\n")
        # pprint(queries)
        # pprint(result_df)
        if type(result_df) == type(""):
            return result_df
        return {
            "name" : "user_longest_avg_msg_length",
            "desciption": "What discord user has the longest average message length in a particular guild?",
            "uuid": selected_query["uuid"],
            "fig" : go.Figure(
                data=[
                    go.Bar(
                        name='Average Content Length',     
                        x=result_df["nickname"], 
                        yaxis='y',
                        y = result_df["content_length"], 
                        offsetgroup=1, 
                        orientation='v'
                    ),
                    go.Bar(
                        name='Content Count',  
                        x=result_df["nickname"], 
                        yaxis='y2', 
                        y = result_df["content_count"],
                        offsetgroup=2, 
                        orientation='v'
                    )
                ],
                layout={
                    'yaxis':  {'title': 'Average Content Length'},
                    'yaxis2': {'title': 'Content Count', 'overlaying': 'y', 'side': 'right'}
                }
                
            ),
            "layout" : go.Layout(
                barmode='group',
                title='Messages length and count for Question Messages',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }