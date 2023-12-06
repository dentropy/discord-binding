import React from 'react';
import Plot from 'react-plotly.js';

import { Context } from './Provider';


export default function PlotlyChart(props){
  const [context, setContext] = React.useContext(Context);
  console.log("PlotlyChart props")
  console.log(props)
  const [queryDescription, setQueryDescription] = React.useState({
    label : "Getting Data",
    query_data : {
      description : "Loading...."
    }
  })
  const [graphData, setGraphData] = React.useState([
    {
      x: [1, 2, 3, 4, 5],
      y: [10, 15, 13, 18, 20],
      type: 'scatter',
      mode: 'lines+markers',
      marker: { color: 'red' },
    },
  ])
  const [graphLayout, setGraphLayout] = React.useState({
    title: 'Sample Chart',
    xaxis: { title: 'X Axis' },
    yaxis: { title: 'Y Axis' },
  })

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
        form_data.append('graph_name', context.select_data_visualization.query_name);
        // console.log("context.select_guild")
        // console.log(context.select_guild.guild_id)
        form_data.append('guild_id',   String(context.select_guild.guild_id) );
        // console.log("context.select_channel")
        // console.log(context.select_channel)
        form_data.append('channel_id', String(context.select_channel.channel_id));
        console.log("context.select_author")
        console.log(context.select_author)
        form_data.append('author_id',  String(context.select_author.author_guild_id) );
        const options = {
          method: 'POST',
          body: form_data
        };
        console.log("plotly_post_options")
        for (var value of form_data.values()) {
              console.log(value);
        }
        fetch("/plotly_graph", options)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          
          console.log('POST request successful for Data Visualization Data! PlotlyChart:', data);
          console.log(JSON.parse(data.fig))
          let graph_data = JSON.parse(data.fig).data
          setGraphData(graph_data)
          let tmp_layout = JSON.parse(data.layout)
          // console.log("data.fig.layout")
          // console.log(graph_data) 
          // Object.keys(JSON.parse(graph_data.layout)).forEach(((element) => {
          //   console.log("data.fig.layout")
          //   console.log(element) 
          // }))
          tmp_layout.width = props.graphWidth //window.innerWidth / 12 * 12 - 20
          tmp_layout.height = window.innerHeight - 250
          setGraphLayout(tmp_layout)
          setQueryDescription(context.select_data_visualization)
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
    <div>
      <h2>{context.select_data_visualization.query_data.desciption}</h2>
      {/* <h2>{JSON.stringify(context.select_data_visualization.query_data)}</h2> */}
      <Plot data={graphData} layout={graphLayout} />
    </div>
  );
};

