import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

from pprint import pprint
import pandas as pd

from modules.query_resolver import query_resolver
from modules.queries import queries

def build_graph(pg_cursor, graph_name, query_args_dict):
    graph_names = [
        "user_longest_avg_msg_length"
    ]
    if graph_name not in graph_names:
        return f"Error: {graph_name} is not in graph_names \n {graph_names}"
    if graph_name == "user_longest_avg_msg_length":
        result_df = query_resolver(pg_cursor, queries, "user_longest_avg_msg_length", query_args_dict)
        # pprint(result_df)
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
                title='Message Counts',
                autosize=False,
                width=1024 * 2,  # Width in pixels
                height=800   # Height in pixels
            )
        }
