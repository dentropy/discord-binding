``` sql
CREATE TABLE bucketmodel (
  key INTEGER PRIMARY KEY AUTOINCREMENT, 
  id VARCHAR(255), created DATETIME, 
  name VARCHAR(255), type VARCHAR(255), 
  client VARCHAR(255), 
  hostname VARCHAR(255)
);
```

``` sql
CREATE TABLE eventmodel (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  bucket_id INTEGER, 
  timestamp DATETIME, 
  duration DECIMAL(10, 5), 
  datastr VARCHAR(255)
  );
```


``` sql
CREATE TABLE channels (
  index_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  channel_id     VARCHAR(255), 
  channel_type   VARCHAR(255), 
  categoryId     VARCHAR(255), 
  category       VARCHAR(255), 
  catagory_name  VARCHAR(255),
  catagory_topic VARCHAR(255)
  );
```

``` sql
CREATE TABLE guilds (
  index_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  id VARCHAR(255), 
  bucket_id INTEGER, 
  timestamp DATETIME, 
  duration DECIMAL(10, 5), 
  datastr VARCHAR(255)
  );
```

``` sql
CREATE TABLE messages (
  index_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  id VARCHAR(255), 
  bucket_id INTEGER, 
  timestamp DATETIME, 
  duration DECIMAL(10, 5), 
  datastr VARCHAR(255)
  );
```

## WAIT

``` sql
DROP TABLE messages;
DROP TABLE guilds;
DROP TABLE channels;
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
