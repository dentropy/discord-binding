
## dotenv settings

``` bash

db_select='neo4j'
db_url='bolt://neo4j:neo4j@localhost:7687'

```

## TO Access the Web Console

http://localhost:7474/browser/

## Example Queries


``` bash

Match (Authors)-[Guilds]->(Channels)
Return Authors,Guilds,Channels;


```

## List Authors, Guilds, and Channels

``` json

MATCH (startNode:Authors)-[:author_guild]->(midNode:Guilds)<-[:guild_channel]-(endNode:Channels)
RETURN startNode, midNode, endNode LIMIT 25

```
## Users that posted in a specific channel 



``` json



```


## What messages reply to one another

``` json

MATCH (reply:Messages) - [:reply_to_message] -> (op:Messages) return reply, op

```

## Authors who reply to one another via Messages

``` json

MATCH (a:Authors) <- [:message_author_id] - (b:Messages) - [:reply_to_message] -> (c:Messages) - [:message_author_id] -> (d:Authors) return a, b, c, d limit 300

```

## Messages and Author and how they connect

``` json

MATCH p=()-[r:message_author_id]->() RETURN p LIMIT 100

```

## Delete everything in database

``` bash

MATCH (n)
DETACH DELETE n

```

## Reminders

``` bash

neomodel_inspect_database --db bolt://neo4j:neo4j@127.0.0.1:7687 --write-to neo4j_schema.txt


neomodel_install_labels ./schemas/schema_neo4j.py --db bolt://neo4j:neo4j@127.0.0.1:7687

```