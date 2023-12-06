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


import { Context } from './Provider';
import PlotlyChart from './PlotlyChart';


import SelectGuild from './SelectGuild'
import SelectChannel from './SelectChannel';
import SelectAuthor from './SelectAuthor';
import SelectDataVisualization from './SelectDataVisualization';
import SelectRender from './SelectRender'
import SelectDiscordData from './SelectDiscordData';
function App() {
  // const [count, setCount] = React.useState(0)
  const [ data, setData ] = React.useState("Fetching Data")
  const [context, setContext] = React.useContext(Context);
  return (
    <>
      <MainAppBar />
      <Box sx={{ flexGrow: 1, p: 2 }} >
        <Grid container spacing={2} >
          {/* <Grid xs={3}>
            <SelectDiscordData />
          </Grid> */}
          <Grid xs={12}>
            {/* <PlotlyChart /> */}
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
