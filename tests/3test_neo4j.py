from neomodel import config, db
from pprint import pprint
config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'  # default
db.set_connection()
results, meta = db.cypher_query("RETURN 'Hello World' as message")
pprint(results)