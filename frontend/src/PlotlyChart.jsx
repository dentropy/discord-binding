import React from 'react';
import Plot from 'react-plotly.js';

export default function PlotlyChart(){
  // Define your data for the chart
  const data = [
    {
      x: [1, 2, 3, 4, 5],
      y: [10, 15, 13, 18, 20],
      type: 'scatter',
      mode: 'lines+markers',
      marker: { color: 'red' },
    },
  ];

  // Define layout options for the chart
  const layout = {
    title: 'Sample Chart',
    xaxis: { title: 'X Axis' },
    yaxis: { title: 'Y Axis' },
  };

  return (
    <div>
      <h2>Plotly Chart Example</h2>
      <Plot data={data} layout={layout} />
    </div>
  );
};

