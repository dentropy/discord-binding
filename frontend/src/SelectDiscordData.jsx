import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from './Provider';
import Button from '@mui/material/Button';

export default function SelectDiscordData() {
  const [context, setContext] = React.useContext(Context);
  const [guildData, setGuildData] = React.useState(
    {
        options : [{ label : "Fetching Data", id : 0 }],
        selected_value : { label : "Fetching Data", id : 0 },
        value : "Fetching Data"
    }
  )
  const [channelData, setChannelData] = React.useState(
    {
        options : [{ label : "Fetching Data", id : 0 }],
        selected_value : { label : "Fetching Data", id : 0 },
        value : "Fetching Data"
    }
  )
  const [authorData, setAuthorData] = React.useState(
    {
        options : [{ label : "Fetching Data", id : 0 }],
        selected_value : { label : "Fetching Data", id : 0 },
        value : "Fetching Data"
    }
  )
  const [dataVisualization, setDataVisualization] = React.useState(
    {
        options : [{ label : "Fetching Data", id : 0 }],
        selected_value : { label : "Fetching Data", id : 0 },
        value : "Fetching Data"
    }
  )

  React.useEffect(
    () => {
        fetch_guilds()
    },
    []
  )
  function fetch_guilds(){
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
      console.log('POST request successful for Guild Data! Response data:', data);
      setGuildData({
        options : data,
        selected_value : data[0],
        value : data[0].label
      })
      fetch_channels(data[0].guild_id)
      setContext({
        type: 'SELECT_GUILD',
        payload: data[0]
      })
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  function fetch_channels(guild_id){
    console.log("Fetch Channels")
    const form_data = new FormData();
    form_data.append('query_name', 'guild_channels');
    form_data.append('guild_id', guild_id);
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
      console.log('POST request successful for Channel Data! Response data:', data);
      if(data.length != 0){
        console.log("Fetched new Channel Data")
        console.log(data)
        setChannelData({
            options : data,
            selected_value : data[0],
            value : data[0].label
          })
        fetch_authors(guild_id)
        setContext({
          type: 'SELECT_CHANNEL',
          payload: data[0]
        })
      }
    })
    .catch(error => {
      console.error('Error:', error);
    })
  }
  function fetch_authors(guild_id){
    console.log("Fetch Authors")
    const form_data = new FormData();
    form_data.append('query_name', 'guild_authors');
    form_data.append('guild_id', guild_id);
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
      console.log('POST request successful for Author Data! Response data:', data);
      if(data.length != 0){
        console.log("Fetched new Channel Data")
        console.log(data)
        setAuthorData({
            options : data,
            selected_value : data[0],
            value : data[0].label
          })
        console.log(`AUTHOR_DATA_GOT\n ${JSON.stringify(data[0])}`)
        setContext({
          type: 'SELECT_AUTHOR',
          payload: data[0]
        })
        fetch_data_visualization()
      }
    })
    .catch(error => {
      console.error('Error:', error);
    })
  }
  function fetch_data_visualization(){
    const options = {
        method: 'GET'
      };
      fetch("/list_graphs", options)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('POST request successful for Data Visualization Data! Response data:', data);
        if(data.length != 0){
          console.log("list_graphs")
          console.log(data)
          setDataVisualization({
            options : data,
            selected_value : data[0],
            value : data[0].label
          })
          setContext({
            type: 'SELECT_DATA_VISUALIZATION',
            payload: data[0]
          })
        }
      })
      .catch(error => {
        console.error('Error:', error);
      })
  }

  function set_guild(input, value){
    guildData.selected_value = value
    setGuildData(guildData)
    setContext({
        type: 'SELECT_GUILD',
        payload: value
      })
  }
  function set_channel(input, value){
    console.log("set_channel")
    console.log(value)
    let newChannel = JSON.parse(JSON.stringify(channelData));
    newChannel.selected_value = value
    console.log(newChannel)
    setChannelData(newChannel)
    setContext({
        type: 'SELECT_CHANNEL',
        payload: value
      })
  }
  function set_author(input, value){
    console.log("set_author")
    console.log(value)
    let save_i = 0
    let newAuthor = JSON.parse(JSON.stringify(authorData));
    newAuthor.selected_value = value
    newAuthor.value = value.label
    console.log(newAuthor)
    setAuthorData(newAuthor)
    setContext({
        type: 'SELECT_AUTHOR',
        payload: value
      })
  }
  function set_data_visualization(input, value) {
    console.log("set_data_visualization")
    console.log(value)
    let newAuthor = JSON.parse(JSON.stringify(dataVisualization));
    newAuthor.selected_value = value
    newAuthor.value = value.label
    console.log(newAuthor)
    setDataVisualization(newAuthor)
    setContext({
        type: 'SELECT_DATA_VISUALIZATION',
        payload: value
    })
  }
  function update_render() {
    // console.log("UDPATE RENDER_NOW")
    setContext({
        type: 'RENDER_NOW',
        payload: true
    })
  }
  return (
    <>
        <Autocomplete
        disablePortal
            id="autocomplete_select_guild"
            onChange={set_guild}
            options={guildData.options}
            value={guildData.selected_value}
            isOptionEqualToValue={(option, value) => option.guild_id === value.guild_id}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Guild" />}
        />
        <Autocomplete
            disablePortal
            id="autocomplete_select_channel"
            onChange={set_channel}
            options={channelData.options}
            value={channelData.selected_value}
            isOptionEqualToValue={(option, value) => option.channel_id === value.channel_id}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Channel" />}
        />
        <Autocomplete
            disablePortal
            id="autocompelte_select_author"
            isOptionEqualToValue={(option, value) => option.author_guild_id === value.author_guild_id}
            onChange={set_author}
            options={authorData.options}
            value={authorData.selected_value}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Author" />}
        />
        <Autocomplete
            disablePortal
            id="autocomplete_select_data_visualization"
            onChange={set_data_visualization}
            options={dataVisualization.options}
            value={dataVisualization.selected_value}
            isOptionEqualToValue={(option, value) => option.query_name == value.query_name}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Data Visualization" />}
        />
        <Button variant="outlined" onClick={update_render}>Render Data Visualization</Button>
        {/* {JSON.stringify(channelData.selected_value)}
        <br /><br /> */}
        {/* {JSON.stringify(authorData.selected_value)}
        <br></br>  */}
        {/* {JSON.stringify(dataVisualization)}
        <br></br>  */}
    </>
  );d
}

const top100Films = [
    { label: 'The Shawshank Redemption', year: 1994 },
    { label: 'The Godfather', year: 1972 },
    { label: 'The Godfather: Part II', year: 1974 },
    { label: 'The Dark Knight', year: 2008 },
    { label: '12 Angry Men', year: 1957 },
    { label: "Schindler's List", year: 1993 }
]