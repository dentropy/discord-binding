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


from tests.postgresql_query_test import test_queries
from modules.query_resolver import query_resolver
from modules.query_resolver import check_query_select
from modules.queries import queries

import json

from django.views.decorators.csrf import csrf_exempt

from modules.graphs import build_graph, list_graphs, graph_names


@csrf_exempt
def list_labels(request):
    result = query_resolver(cursor, queries, "list_labels")

@csrf_exempt
def add_label(request):
    label_name = request.POST.get('label_name')
    label_description= request.POST.get('label_description')
    cursor.execute("""
    INSERT INTO labels_t
        (
            label_name,
            label_description
        )
    VALUES (%s, %s)
    """, (label_name, label_description))
    connection.commit()
    return JsonResponse({"status" : "True"}, safe=False)
