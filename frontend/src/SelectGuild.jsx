import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from './Provider';

export default function SelectGuild() {
  const [context, setContext] = React.useContext(Context);
  function set_guild(input, value) {
    setContext({
        type: 'SELECT_GUILD',
        payload: value
    })
  }
  React.useEffect(
    () => {
      const form_data = new FormData();
      form_data.append('query_name', 'list_guilds');
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
        console.log('POST request successful for Guild Data! Response data:', data);
        setContext({
          type: 'SET_GUILDS',
          payload: data
        })
        setContext({
          type: 'SELECT_GUILD',
          payload: data[0]
        })
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },
    []
  )

  return (
    <Autocomplete
      disablePortal
      id="select_guild_autocomplete"
      onChange={set_guild}
      options={context.guilds}
      value={context.guilds[0]}
      sx={{ width: 300 }}
      renderInput={(params) => <TextField {...params} label="Guild" />}
    />
  );
}

const top100Films = [
    { label: 'The Shawshank Redemption', year: 1994 },
    { label: 'The Godfather', year: 1972 },
    { label: 'The Godfather: Part II', year: 1974 },
    { label: 'The Dark Knight', year: 2008 },
    { label: '12 Angry Men', year: 1957 },
    { label: "Schindler's List", year: 1993 }
]