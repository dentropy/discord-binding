import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Avatar from '@mui/material/Avatar';
import Grid from '@mui/material/Grid';
// import { makeStyles } from '@mui/styles';
// const useStyles = makeStyles((theme) => ({
//     root: {
//       padding: theme.spacing(2),
//       display: 'flex',
//       alignItems: 'center',
//     },
//     avatar: {
//       marginRight: theme.spacing(2),
//     },
//   }));
  
function Message({ text, sender, avatarUrl }) {
  // const classes = useStyles();

  return (
    <Paper elevation={3}>
      <Grid container wrap="nowrap">
        <Grid item>
          <Avatar alt={sender} src={avatarUrl} />
        </Grid>
        <Grid item>
          <Typography variant="body1">
            <strong>{sender}</strong>
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {text}
          </Typography>
        </Grid>
      </Grid>
    </Paper>
  );
}
  
  export default Message;
  