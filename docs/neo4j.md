``` bash

neomodel_inspect_database --db bolt://neo4j:neo4j@127.0.0.1:7687 --write-to neo4j_schema.txt


neomodel_install_labels schema_neo4j.py --db bolt://neo4j:neo4j@127.0.0.1:7687


```


``` bash

db_url='bolt://neo4j:neo4j@localhost:7687'

```

http://localhost:7474/browser/

``` cypher

Match (Authors)-[Guilds]->(Channels)
Return Authors,Guilds,Channels;

```

## Delete everything in database

``` bash

MATCH (n)
DETACH DELETE n

```