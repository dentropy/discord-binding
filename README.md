
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

## Helpers

You can check if the SQLite database is being written to with `ls -lrt` a couple times in the directory of the database to see if it is increasing.