import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from './Provider';

export default function SelectQuery() {
  const [context, setContext] = React.useContext(Context);

  function set_query(input, value) {
    console.log(value)
    setContext({
        type: 'SELECT_QUERY',
        payload: value
    })
  }
  React.useEffect(
    () => {
      if(context.select_guild.label != "Getting Data"){
        const form_data = new FormData();
        form_data.append('query_name', 'guild_authors');
        form_data.append('guild_id', context.select_guild.guild_id);
        const options = {
          method: 'POST',
          body: form_data
        };
        fetch("/query", options)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log('POST request successful! Response data:', data);
          setContext({
            type: 'SET_QUERIES',
            payload: data
          })
          setContext({
            type: 'SELECT_QUERY',
            payload: data[0]
          })
        })
        .catch(error => {
          console.error('Error:', error);
        })
      }
    },
    [context.select_guild]
  )
  return (
    <>
        <Autocomplete
            disablePortal
            onChange={set_query}
            id="select_query_autocomplete"
            options={context.queries}
            value={context.queries[0]}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Query" />}
        />
    </>
  );
}
