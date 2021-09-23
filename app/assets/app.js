import { bb, line } from 'billboard.js';
import "billboard.js/dist/billboard.css";

import "tailwindcss/tailwind.css"


window.onload = () => {
  document.querySelectorAll('.graph').forEach((graph) => {
    const state = graph.dataset.state;
    const labels = JSON.parse(graph.dataset.labels);
    const values = JSON.parse(graph.dataset.values);
    const maxY = parseInt(graph.dataset.maxY);

    var chart = bb.generate({
      bindto: `#graph-${state}`,
      data: {
        type: line(),
        x: 'Date',
        xFormat: "%Y-%m-%d",
        columns: [
          ["Date"].concat(labels),
          ["Cases"].concat(values),
        ],
      },
      line: {
        point: false,
      },
      axis: {
        x: {
          type: 'timeseries',
          tick: {
            format: '%e %b %Y',
          },
        },
        y: {
          max: maxY,
        },
      },
    });
  });
};
