## Discord Binding

The goal of this project is to take the data exported form [Tyrrrz/DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) and put it into a relational database so aggregations can be easily calculated and so the data can be used in other parts of an ETL pipeline.

## Getting the Discord Data

``` bash
cd /path/to/discord/data
DISCORD_TOKEN="Jibberish"
export_folder="DiscordAccountName"
mkdir $export_folder
cd $export_folder
my_dir="pwd"
docker run --rm -v $(pwd)/$export_folder:/out \
	--name discord02 \
	tyrrrz/discordchatexporter:stable exportall \
	-t $DISCORD_TOKEN \
	--media \
	--dateformat "yyyy-MM-dd H:mm:ss.ffff" \
	-f Json -p 80mb
```

## Transforming the data from [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)

**Single Guild**

Copy .env_example to .env
Set `guild_path` and `db_url` in .env file
`guild_path` is the directory of the DiscordChatExporter json files
`db_url` is the path of the sqlite database you want to save the messages to

``` bash

python3 guild_json_to_sqlite.py

```

Wait and voila

**Directory of Guild's**

Copy .env_example to .env
Set `guild_directory_path`
`guild_directory_path` is the directory of guilds exported from DiscordChatExporter 

``` bash

python3 guild_directory_to_sqlite.py > logs-$(date +"%Y-%m-%d_%H-%M-%S").out

```

Wait and voila



## Transforming SQLite data

Just getting the JSON data into sqlite is not enough we need proper SQL rows and columns.

**Single Guild**

``` bash

python3 fix_schema.py $PATH_TO_SQLITE_DATABASE

```

**Directory of SQLite files**

When using default out folder inside this directory run,

``` bash

bash fix_schemas.sh

```

## Postgres Migration

* Run Postgres

``` bash
wget https://gist.githubusercontent.com/dentropy/e408f86de7261a516af9bb43234ae343/raw/b7c1373bff0152fc59c246e8af0a7f7d48bc340b/postgres2.yml
docker-compose -f postgres2.yml up -d
docker-compose -f postgres2.yml logs -f
```

* Access Postgres

``` bash

psql postgresql://postgres:postgres@127.0.0.1:5432/postgres

# or

docker exec -it postgres2 psql -U postgres

```

* Create Database

``` bash
CREATE DATABASE discorddata;

\c discorddata

exit;
```

``` bash

psql postgresql://postgres:postgres@127.0.0.1:5432/discorddata

exit;
```

* Create Tables

Set postgres_url in .env

``` bash

python3 postgres_schema.py

```

* Load sqlite databases

``` bash

bash postgres_load.sh

```


* Setup [PostGraphile](https://www.graphile.org/postgraphile/usage-cli/)


``` bash
# Install
npm install -g postgraphile @graphile/pg-aggregates

# Run
postgraphile --append-plugins @graphile/pg-aggregates --enhance-graphiql -c postgresql://postgres:postgres@127.0.0.1:5432/discorddata

```

## Helpers

You can check if the SQLite database is being written to with `ls -lrt` a couple times in the directory of the database to see if it is increasing.


## Example postgraphile queries

``` graphql

{
  allChannelsTs{
    nodes {
      id,
      channelName,
      guildId,
      guildsTByGuildId{
        id,
        guildName
      }
    }
  }
}

```


``` graphql

query MyQuery {
  allGuildsTs {
    aggregates {
      distinctCount {
        id
      }
    }
  }
  allMessagesTs {
    aggregates {
      distinctCount {
        id
      }
    }
  }
  allChannelsTs {
    aggregates {
      distinctCount {
        id
      }
    }
  }
}

```
## Fix the timestamps!



``` SQL
ALTER TABLE messages_t
ADD COLUMN real_timestamp timestamp WITHOUT TIME ZONE;

ALTER TABLE messages_t
ADD COLUMN real_timestamp_edited timestamp WITHOUT TIME ZONE;

UPDATE messages_t
SET real_timestamp = to_timestamp(unix_timestamp);

UPDATE messages_t
SET real_timestamp_edited = to_timestamp(unix_timestampEdited)
WHERE unix_timestampEdited IS NOT NULL;

ALTER TABLE messages_t
  ADD CONSTRAINT messages_t_to_guild_id
  FOREIGN KEY (guild_id)
  REFERENCES guilds_t(id)
  ON DELETE CASCADE;
CREATE INDEX ON messages_t (guild_id);
```

## DON'T RUN THIS

``` SQL
ALTER TABLE messages_dump_t
DROP COLUMN #real_timestamp;
```
