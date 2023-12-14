import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
// import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Unstable_Grid2';

import SelectDiscordData from './SelectDiscordData'
import PlotlyChart from './PlotlyChart';

import { Context } from './Provider';
import SelectDataVisualization from './SelectDataVisualization'

const drawerWidth = 375;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth * 2}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: `-${drawerWidth}px`
    }),
  }),
);

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function PersistentDrawerLeft() {
  const theme = useTheme();
  const [context, setContext] = React.useContext(Context);
  const [open, setOpen] = React.useState(false);
  const [openRight, setOpenRight] = React.useState(false);
  const [graphWidth, setGraphWidth] = React.useState(0)//window.innerWidth / 12 * 12 - 20);
  function update_render() {
    // console.log("UDPATE RENDER_NOW")
    setContext({
        type: 'RENDER_NOW',
        payload: true
    })
  }
  const handleDrawerOpen = () => {
    setGraphWidth(graphWidth - drawerWidth)
    // console.log(graphWidth)
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setGraphWidth(graphWidth + drawerWidth)
    // console.log(graphWidth)
    setOpen(false);
  };

  const handleDrawerOpenRight = () => {
    setGraphWidth(graphWidth + drawerWidth)
    // console.log(graphWidth)
    setOpenRight(true);
  };

  const handleDrawerCloseRight = () => {
    setGraphWidth(graphWidth - drawerWidth)
    // console.log(graphWidth)
    setOpenRight(false);
  };

  return (
    <div style={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar style={{left : 0}}>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Discord Binding
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          </Typography>
          <br />
            {
              //style={{transform: 'translate(50%, 0%)'}}
            }
          <Button variant="contained"  onClick={update_render}>Render Data Visualization</Button>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpenRight}
            edge="start"
            sx={{ mr: 2, ...(openRight && { display: 'none' }) }}
          >
            <MenuIcon style={{position: "absolute", right : - window.innerWidth  + 600 - graphWidth}}/>
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        < SelectDiscordData />

        <Divider />
      </Drawer>

      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="right"
        open={openRight}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerCloseRight}>
            {theme.direction === 'rtr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <SelectDataVisualization />
        <Divider />
      </Drawer>


      <Main open={open}>
        <DrawerHeader />
        <div sx={{ flexGrow: 1, p: 2 }} >
        <Grid container spacing={2} >
          {/* <Grid xs={3}>
            <SelectDataVisualization />
          </Grid> */}
          <Grid xs={12}>
            <PlotlyChart graphWidth={(window.innerWidth / 12 * 12 - 20) + graphWidth  }/>
          </Grid>
        </Grid>
      </div>
      </Main>
    </div>
  );
}