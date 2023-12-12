import React from 'react';
import Message from './Message';
import { Context } from './Provider';
import Grid from '@mui/material/Grid';
import SelectDiscordData from './SelectDiscordData';
function Messages() {
    const [context, setContext] = React.useContext(Context);

    return (
      <>
        <Grid container spacing={2}>
            <Grid item xs={4}>
                <h1>Messages</h1>
                <SelectDiscordData />
            </Grid>
            <Grid item xs={8}>
                <Message
                    sender="John Doe"
                    text="Hello, how are you doing?"
                    avatarUrl="https://example.com/avatar.jpg"
                />
                <Message
                    sender="Jane Smith"
                    text="I'm doing great, thanks for asking!"
                    avatarUrl="https://example.com/avatar2.jpg"
                />
            </Grid>
        </Grid>

      </>
    )
  }
  
  export default Messages
  