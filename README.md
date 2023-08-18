
## Access Postgres

``` bash
docker exec -it postgres2 psql -U postgres
```

## DROP TABLES

``` sql
DROP TABLE messages;
DROP TABLE guilds;
DROP TABLE channels;
DROP TABLE embeds;
DROP TABLE embeds;
DROP TABLE embeds;
```


## Get my messages in the order I sent them

``` sql

SELECT DISTINCT content, timestamp
FROM messages
INNER JOIN authors ON messages.author = authors.id
WHERE authors.name = 'dentropy'
ORDER BY timestamp ASC;


```

## Get the longest messages and the person who sent them

``` sql

SELECT DISTINCT content, authors.name
FROM messages
INNER JOIN authors ON messages.author = authors.id
ORDER BY LENGTH(content) DESC;

```

## Get my messages ordered by length

``` sql

SELECT DISTINCT content, timestamp
FROM messages
INNER JOIN authors ON messages.author = authors.id
WHERE authors.name = 'dentropy'
ORDER BY LENGTH(content) DESC;

```

## Most Reactions


``` sql

SELECT count, content, name
FROM reactions
INNER JOIN messages ON messages.id = reactions.message_id
INNER JOIN authors ON messages.author = authors.id
GROUP BY message_id
order by count desc;

```

## Total Number of Messages

``` sql

SELECT COUNT(*) FROM messages;

```

## Embeddings Stuff

``` sql
DROP TABLE cohere_embeddings_t;
```

## Vector Databases to Try

* [qdrant/qdrant-client: Python client for Qdrant vector search engine](https://github.com/qdrant/qdrant-client)
* [milvus-io/milvus: A cloud-native vector database, storage for next generation AI applications](https://github.com/milvus-io/milvus)
* [marqo-ai/marqo: Vector search for humans.](https://github.com/marqo-ai/marqo)
