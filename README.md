## DROP TABLES

``` sql
DROP TABLE messages;
DROP TABLE guilds;
DROP TABLE channels;
DROP TABLE embeds;
DROP TABLE embeds;
DROP TABLE embeds;
```


## Get my messages

``` sql

SELECT DISTINCT content, timestamp
FROM messages
INNER JOIN authors ON messages.author = authors.id
WHERE authors.name = 'dentropy'
ORDER BY timestamp ASC;


```

``` sql

SELECT DISTINCT content, authors.name
FROM messages
INNER JOIN authors ON messages.author = authors.id
ORDER BY LENGTH(content) DESC;

```
