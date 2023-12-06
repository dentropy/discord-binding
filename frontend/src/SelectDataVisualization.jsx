import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { Context } from './Provider';

export default function SelectDataVisualization() {
  const [context, setContext] = React.useContext(Context);
  const [dataVisualizationTags, setDataVisualizationsTags] = React.useState(
    { label : "Getting Data" }
  )
  const [rawDataVisualizationTags, setRawDataVisualizationsTags] = React.useState()
  const [dataVisualizations, setDataVisualizations] = React.useState({
    label : "Getting Data",
    description : "Loading...",
    query_data : {
      description : "Loading...."
    }
  })
  function set_data_visualization_via_tag(input, value) {
    if (value.label == "None") {
      setDataVisualizations(rawDataVisualizationTags)
    }
    else {
      let query_selection = []
      rawDataVisualizationTags.forEach((query) => {
        if(query.tags.includes(value.label)){
          console.log("value.label in set_data_visualization_via_tag")
          console.log(value.label)
          query_selection.push(query)
        }
      })
      setDataVisualizations(query_selection)
    }
  }
  function set_data_visualization(input, value) {
    console.log("set_data_visualization")
    console.log(value)
    setContext({
        type: 'SELECT_DATA_VISUALIZATION',
        payload: value
    })
  }
  React.useEffect(
    () => {
      if(context.select_guild.label != "Getting Data"){
        // const form_data = new FormData();
        // form_data.append('query_name', 'guild_channels');
        // form_data.append('guild_id', context.select_guild.guild_id);
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
            let tags = ["None"]
            let tag_labels = [{label : "None"}]
            data.forEach( (graph_element) => {
              // console.log("graph_element")
              // console.log(graph_element)
              // console.log(graph_element.tags)
              graph_element.tags.forEach( (tag_element) => {
                if(!tags.includes(tag_element)){
                  tags.push(tag_element)
                  tag_labels.push({
                    label : tag_element
                  })
                }
              })
            })
            // console.log("tags")
            // console.log(tags)
            setDataVisualizationsTags(tag_labels)
            setDataVisualizations(data)
            setRawDataVisualizationsTags(data)
            // setContext({
            //   type: 'SET_DATA_VISUALIZATIONS',
            //   payload: data
            // })
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
    },
    [context.select_guild]
  )
  return (
    <>
      <Autocomplete
        disablePortal
        id="select_data_disualization_tag_autocomplete"
        onChange={set_data_visualization_via_tag}
        options={dataVisualizationTags}
        value={dataVisualizations[0]}
        sx={{ width: 355 }}
        renderInput={(params) => <TextField {...params} label="Narrow Query Selection via Tag" />}
      />
      <Autocomplete
        disablePortal
        id="select_data_disualization_autocomplete"
        onChange={set_data_visualization}
        options={dataVisualizations}
        value={dataVisualizations[0]}
        sx={{ width: 355 }}
        renderInput={(params) => <TextField {...params} label="Data Visualization" />}
      />
    </>
  );
}

const top100Films = [
    { label: 'The Shawshank Redemption', year: 1994 },
    { label: 'The Godfather', year: 1972 },
    { label: 'The Godfather: Part II', year: 1974 },
    { label: 'The Dark Knight', year: 2008 },
    { label: '12 Angry Men', year: 1957 },
    { label: "Schindler's List", year: 1993 }
]