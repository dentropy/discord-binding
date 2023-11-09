# Setup Postgres

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

Set postgres_url `postgresql://postgres:postgres@127.0.0.1:5432/discorddata` in .env


## Check currently running queries

``` sql
SELECT datname, pid, state, query, age(clock_timestamp(), query_start) AS age 
FROM pg_stat_activity
WHERE state <> 'idle' 
    AND query NOT LIKE '% FROM pg_stat_activity %' 
ORDER BY age;
```

## Reset Postgres

``` sql
\c postgres
DROP DATABASE discorddata;
CREATE DATABASE discorddata;
\c discorddata
dt
```