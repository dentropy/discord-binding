import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from './Provider';

export default function SelectChannel() {
  const [context, setContext] = React.useContext(Context);
  function set_channel(input, value) {
    setContext({
        type: 'SELECT_CHANNEL',
        payload: value
    })
  }
  React.useEffect(
    () => {
      if(context.select_guild.label != "Getting Data"){
        const form_data = new FormData();
        form_data.append('query_name', 'guild_channels');
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
            type: 'SET_CHANNELS',
            payload: data
          })
          setContext({
            type: 'SELECT_CHANNEL',
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
    <Autocomplete
      disablePortal
      id="select_channel_autocomplete"
      onChange={set_channel}
      options={context.channels}
      value={context.select_channel.label}
      sx={{ width: 300 }}
      renderInput={(params) => <TextField {...params} label="Channel" />}
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