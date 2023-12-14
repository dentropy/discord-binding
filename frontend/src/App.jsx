import * as React from 'react';
// import Box from "@mui/material/Box";
import Grid from '@mui/material/Grid';

import MainAppBar from './MainAppBar'
import Provider from './Provider';
import SelectDiscordData from './SelectDiscordData';
import PlotlyChart from './PlotlyChart';
function App() {
  return (
    <>
      <Provider>
      <MainAppBar />
      </Provider>
    </>
  )
}

export default App

