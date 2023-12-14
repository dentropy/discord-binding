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
    const [messageData, setMessageData] = React.useState([]);
    const [messages, setMessages] = React.useState(<>
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
    </>)
    React.useEffect(
        () => {
          // setContext({
          //     type: 'RENDER_NOW',
          //     payload: false
          // })
          // Get what we want rendered
          if(context.select_guild.label != "Getting Data"){
            const form_data = new FormData();
            // console.log("context.select_data_visualization")
            // console.log(context.select_data_visualization)
            form_data.append('query_name', "channel_messages");
            form_data.append('offset', 0);
            // console.log("context.select_guild")
            // console.log(context.select_guild.guild_id)
            form_data.append('order',   "desc" );
            // console.log("context.select_channel")
            // console.log(context.select_channel)
            form_data.append('channel_id', String(context.select_channel.channel_id));
            // console.log("context.select_author")
            // console.log(context.select_author)
            // form_data.append('author_id',  String(context.select_author.author_guild_id) );
            const options = {
              method: 'POST',
              body: form_data
            };
            for (var value of form_data.values()) {
                  console.log(value);
            }
            fetch("/query/", options)
            .then(response => {
              if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
            })
            .then(data => {
              console.log(data)
              setMessageData(data)
              const updated_messages = data.map((mah_message) =>
                        <Message
                            key={mah_message.msg_id}
                            message_id={mah_message.msg_id}
                            sender={mah_message.author_name}
                            timestamp={unixTimeToReadable(mah_message.msg_timestamp)}
                            text={mah_message.msg_content}
                            avatarUrl="https://example.com/avatar.jpg"
                            tags={[
                                {   
                                    id : "5432",
                                    name : "Hello Message"
                                }
                            ]}
                    />
                );
              setMessages(updated_messages)
              setContext({
                type: 'RENDER_NOW',
                payload: false
              })
            })
            .catch(error => {
              console.error('Error:', error);
              setContext({
                type: 'RENDER_NOW',
                payload: false
              })
            })
          }
        },
        [context.render_now]
      )
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
                <Button  variant="outlined">Add Tags to Messages</Button>< br/>
                <Button  variant="outlined">Add Tags to Channel</Button>< br/>
                <Button  variant="outlined">Add Tags to Author</Button>< br/>
            </Grid>
            <Grid item xs={8}>
                <p>{JSON.stringify(context.selected_messages)}</p>
                {messages}
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

  function unixTimeToReadable(timestamp) {
    const date = new Date(timestamp ); // Convert Unix timestamp to milliseconds
  
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Month is zero-based
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
  
    const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    return formattedDate;
  }