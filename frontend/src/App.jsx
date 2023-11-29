import * as React from 'react';
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

// import SelectGuild from './SelectGuild'
// import SelectChannel from './SelectChannel';
// import SelectAuthor from './SelectAuthor';

// import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
// import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';

import MainAppBar from './MainAppBar'

function App() {
  // const [count, setCount] = React.useState(0)
  const [ data, setData ] = React.useState("Fetching Data")

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
        console.log('POST request successful! Response data:', data);
        setData(data)
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },
    []
  )

  return (
    <>
      <MainAppBar />
      <Box sx={{ flexGrow: 1, p: 2 }} >
        <Grid container spacing={2} >
          <Grid xs={12}>
            <h1>Graph Goes Here</h1>
            <h1>This does not line up as I expected</h1>
            <h1>This does not line up as I expected. This does not line up as I expected. This does not line up as I expected. This does not line up as I expected. This does not line up as I expected.</h1>
            {JSON.stringify(data)}
          </Grid>
        </Grid>
      </Box>
      {/* <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
    </>
  )
}

export default App
