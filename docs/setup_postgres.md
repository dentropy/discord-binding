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

Set postgres_url in .env