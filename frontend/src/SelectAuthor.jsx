import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from './Provider';

export default function SelectAuthor() {
  const [context, setContext] = React.useContext(Context);

  function set_author(input, value) {
    setContext({
        type: 'SELECT_AUTHOR',
        payload: value
    })
  }
  return (
    <>
        <Autocomplete
            disablePortal
            onChange={set_author}
            id="combo-box-demo"
            options={context.authors}
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