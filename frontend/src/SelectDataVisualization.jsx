import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from './Provider';

export default function SelectDataVisualization() {
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
        // const form_data = new FormData();
        // form_data.append('query_name', 'guild_channels');
        // form_data.append('guild_id', context.select_guild.guild_id);
        const options = {
          method: 'GET'
        };
        fetch("/list_graphs", options)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log('POST request successful for Data Visualization Data! Response data:', data);
          if(data.length != 0){
            setContext({
              type: 'SET_DATA_VISUALIZATIONS',
              payload: data
            })
            setContext({
              type: 'SELECT_DATA_VISUALIZATION',
              payload: data[0]
            })
          }
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
      id="select_data_disualization_autocomplete"
      onChange={set_channel}
      options={context.data_visualizations}
      value={context.select_data_visualization.label}
      sx={{ width: 300 }}
      renderInput={(params) => <TextField {...params} label="Data Visualization" />}
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