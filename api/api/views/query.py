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

@csrf_exempt
def query(request):
    if request.method == 'POST':
        # Accessing POST data
        query_name = request.POST.get('query_name')
        # print(query_name)
        # print(check_query_select(queries, query_name))
        if(check_query_select(queries, query_name) == False):
            return JsonResponse({'error': 'Invalid request method'})
        print(query_name)
        query_data = {
            "guild_id"   : request.POST.get('guild_id'),
            "channel_id" : request.POST.get('channel_id'),
            "author_id"  : request.POST.get('author_id'),
            "order"      : request.POST.get('order'),
            "offset"     : request.POST.get('offset'),
        }
        result = query_resolver(cursor, queries, query_name, query_data)
        if type(result) == type(""):
            return JsonResponse({'error': result})
        json_result = result.to_json(orient='records')
        return JsonResponse(json.loads(json_result), safe=False)

@csrf_exempt
def list_queries(request):
    return JsonResponse(queries, safe=False)
