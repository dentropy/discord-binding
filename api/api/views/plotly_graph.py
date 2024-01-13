from django.http import JsonResponse

from urllib.parse import urlparse
from pprint import pprint
import pandas as pd
from pprint import pprint

import psycopg2
import psycopg2.extras

import os
from decouple import AutoConfig
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
config = AutoConfig(search_path=current_directory)
url = urlparse(config("db_url"))
connection = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)
cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

import sys
# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))
# Define the path two folders up
two_folders_up = os.path.abspath(os.path.join(current_dir, '../../../'))
# Add the two folders up path to sys.path
sys.path.append(two_folders_up)
# pprint(sys.path)


# from tests.postgresql_query_test import test_queries
from modules.query_resolver import query_resolver
from modules.query_resolver import check_query_select
from modules.queries import queries

import json

from django.views.decorators.csrf import csrf_exempt

from modules.graphs import build_graph, list_graphs, graph_names


@csrf_exempt
def plotly_graph(request):
    if request.method == 'POST':
        # Accessing POST data
        graph_name = request.POST.get('graph_name')
        # print(f"graph_name = {graph_name}")
        graph_args = {
            "guild_id"   : request.POST.get('guild_id'),
            "channel_id" : request.POST.get('channel_id'),
            "author_id"  : request.POST.get('author_id')
        }
        # print("\n\ngraph_args")
        # pprint(graph_args)
        # print(request.POST.get('guild_id'))
        fig = build_graph(
                cursor,
                graph_name,
                graph_args
            )
        # pprint(fig)
        if type(fig) == type(""):
            return JsonResponse({'error': fig})
        fig["fig"] = fig["fig"].to_json()
        fig["layout"] = fig["layout"].to_json()
        return JsonResponse( fig )

@csrf_exempt
def list_graph_data(request):
    return JsonResponse(list_graphs(queries), safe=False)
