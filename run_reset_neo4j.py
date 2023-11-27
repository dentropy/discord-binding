import os
from dotenv import load_dotenv
load_dotenv()

from neomodel import db
db_url = os.environ["db_url"]
print(f"db_url = {db_url}")
# db = db.set_connection(url=os.environ["db_url"])

delete_query = """
MATCH (n)
DETACH DELETE n
"""


db.cypher_query(delete_query)