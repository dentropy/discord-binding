from pprint import pprint
from neomodel import config, db
from schema_neo4j import Guilds, Channels, Authors
db_url = 'bolt://neo4j:neo4j@localhost:7687' # default
db.set_connection(url=db_url)


# results = Authors.nodes.all()# .fetch_relations('guild_channel')
results = Authors.nodes.all().fetch_relations("guild_id")
pprint(results)