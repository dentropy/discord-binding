import React from 'react';
import Plot from 'react-plotly.js';

import { Context } from './Provider';


export default function PlotlyChart(){
  const [context, setContext] = React.useContext(Context);
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
      setContext({
          type: 'RENDER_NOW',
          payload: false
      })
      // Get what we want rendered
      if(context.select_guild.label != "Getting Data"){
        const form_data = new FormData();
        console.log(context.select_data_visualization)
        form_data.append('graph_name', context.select_data_visualization.query_name);
        form_data.append('guild_id',   context.select_guild.guild_id);
        form_data.append('channel_id', context.select_channel.channel_id);
        form_data.append('author_id',  context.select_author.author_id);
        const options = {
          method: 'POST',
          body: form_data
        };
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
          setGraphData(JSON.parse(data.fig).data)
          setGraphLayout(JSON.parse(data.fig).layout)
        })
        .catch(error => {
          console.error('Error:', error);
        })
      }
    },
    [context.render_now]
  )


  return (
    <div>
      <h2>Plotly Chart Example</h2>
      <Plot data={graphData} layout={graphLayout} />
    </div>
  );
};

