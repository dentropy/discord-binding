import * as React from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2';

import MainAppBar from './MainAppBar'
import Provider from './Provider';
function App() {
  return (
    <>
      <Provider>
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
      </Provider>
    </>
  )
}

export default App
