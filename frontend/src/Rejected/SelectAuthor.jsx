import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from '../Provider';

export default function SelectAuthor() {
  const [context, setContext] = React.useContext(Context);

  function set_author(input, value) {
    setContext({
        type: 'SELECT_AUTHOR',
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
          console.log('POST request successful for Author Data! Response data:', data);
          if(data.length != 0){
            console.log("Fetched new Author Data")
            console.log(data)
            setContext({
              type: 'SET_AND_SELECT_AUTHORS',
              payload: data
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
    <>
        <Autocomplete
            disablePortal
            onChange={set_author}
            id="select_author_autocomplete"
            options={context.authors.options}
            value={context.authors.value}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Author" />}
        />
    </>
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