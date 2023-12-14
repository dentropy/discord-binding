import React from 'react';
import { Context } from './Provider';
import Message from './Message';
import Grid from '@mui/material/Grid';
import SelectDiscordData from './SelectDiscordData';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { Button } from '@mui/material';
function Messages() {
    const [context, setContext] = React.useContext(Context);

    return (
      <>
        <Grid container spacing={2}>
            <Grid item xs={4}>
                <h1>Messages</h1>
                <SelectDiscordData />
                <br />
                <TextField id="outlined-basic" label="Outlined" variant="outlined" />
                <Button>Add Tag</Button>
                <Autocomplete
                    disablePortal
                    id="combo-box-demo"
                    options={top100Films}
                    sx={{ width: 300 }}
                    renderInput={(params) => <TextField {...params} label="Movie" />}
                />
                <Button>Add Tags to Messages</Button>< br/>
                <Button>Add Tags to Channel</Button>< br/>
                <Button>Add Tags to Author</Button>< br/>
            </Grid>
            <Grid item xs={8}>
                <p>{JSON.stringify(context.selected_messages)}</p>
                <Message
                    message_id="1234"
                    sender="John Doe"
                    timestamp="2023-12-12 10:10.12"
                    text="Hello, how are you doing?"
                    avatarUrl="https://example.com/avatar.jpg"
                    tags={[
                        {   
                            id : "5432",
                            name : "Hello Message"
                        }
                    ]}
                />
                <Message
                    message_id="4321"
                    sender="Jane Smith"
                    timestamp="2023-12-12 10:10.12"
                    text="I'm doing great, thanks for asking!"
                    avatarUrl="https://example.com/avatar2.jpg"
                    tags={[
                        {   
                            id : "2345",
                            name : "Hello Reply"
                        },
                        {   
                            id : "8909",
                            name : "Test"
                        }
                    ]}
                />
            </Grid>
        </Grid>

      </>
    )
  }
  
  export default Messages
  
  const top100Films = [
    { label: 'The Shawshank Redemption', year: 1994 },
    { label: 'The Godfather', year: 1972 },
    { label: 'The Godfather: Part II', year: 1974 }
  ];