## Discord Binding

The goal of this project is to take the data exported form [Tyrrrz/DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) and put it into a relational database so aggregations can be easily calculated and so the data can be used in other parts of an ETL pipeline.

## Additional Reference Docs

* [Scraping Discord](./docs/discord_scraping.md)
  * This page explains how to get your own Discord data to feed into this ETL pipeline
* [Setup Postgres](./docs/setup_postgres.md)
  * This doc contains instructions to setup and access a local postgres server
* [Setup Postgraphile](./docs/setup_postgraphile.md)
  * Postgraphile generate and runs a graphql API from just looking inside a postgres database
* [neo4j Docs](./docs/neo4j.md)
  * Setup neo4j and contains some example queries, including how to reset the database


## Transforming the data from [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)

Requirements:
- S3 Bucket loaded with data from DiscordChatExporter
- Postgres Database, you can use postgres.dockercompose.yml if you do not have on already setup

Steps:

**Setup python virtual environment and install requirements.txt**

python3.10 minimum unless you install deps manually

``` bash
# install pip
curl https://bootstrap.pypa.io/get-pip.py | python3 $1
python3 -m pip install virtualenv
sudo apt install python3-venv # Debian Distros
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

**Set environment variables using .env file**

``` bash
cp .env_example .env
$EDITOR .env
```

Update the environment variables under `DB Select` and `S3`, the ones below

``` conf
# DB Select
db_select='postgres'
db_url='psql://$USER:$PASS@$HOSTNAME:$PORT/$DATABASE_NAME'

# S3
aws_access_key_id=''
aws_secret_access_key=''
endpoint_url=''
bucket_name=''
```

**Run ETL pipeline, also remember tmux exists**


``` bash
# Using Bash
source env/bin/activate
python3 run_dag.py &
cat *.log
```

