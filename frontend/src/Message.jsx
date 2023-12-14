import React from 'react';
import Paper from '@mui/material/Paper';
import { Context } from './Provider';

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
  
function Message({ text, sender, timestamp, message_id, tags, avatarUrl }) {
  // const classes = useStyles();
  const [context, setContext] = React.useContext(Context);
  const [textColor, setTextColor] = React.useState("white");
  // let textColor = "lightcoral"
  return (
    <Paper elevation={3} style={{backgroundColor: textColor}}>
      <Grid container wrap="nowrap" onClick={() => {
          if (textColor == "white"){
            setTextColor("gray"),
            setContext({
              type: 'ADD_MESSAGE_ID',
              payload: message_id
          })
          }
          else {
            setTextColor("white")
            setContext({
              type: 'REMOVE_MESSAGE_ID',
              payload: message_id
          })
          }
        }
      }>
        <Grid item >
          <Avatar alt={sender} src={avatarUrl} />
        </Grid>
        <Grid item >
          <div>
          <Typography variant="body1" >
            <strong>{sender}</strong> - {timestamp} - {message_id}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {text}
          </Typography>
          {tags.length > 0 &&
            <Typography style={{display : "inline-block"}} variant="body2" color="textSecondary">
              Tags: {tags.map((item) => (
                <li key={item.msg_id}>{item.name}</li>
              ))}
            </Typography>
          }
          </div>
          
        </Grid>
      </Grid>
    </Paper>
  );
}
  
  export default Message;
  