# Setup [PostGraphile](https://www.graphile.org/postgraphile/usage-cli/)


``` bash
# Install
npm install -g postgraphile @graphile/pg-aggregates

# Run
postgraphile --append-plugins @graphile/pg-aggregates --enhance-graphiql -c postgresql://postgres:postgres@127.0.0.1:5432/discorddata


postgraphile --append-plugins @graphile/pg-aggregates,$(pwd)/graphile_time_queries.js --enhance-graphiql -c postgresql://postgres:postgres@127.0.0.1:5432/discorddata
```

``` bash

curl 'http://localhost:5000/graphql' \
  -X POST \
  -H 'content-type: application/json' \
  --data '{"query": "query MyQuery { allGuildsTs { nodes { id guildName } } }"}'

```

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