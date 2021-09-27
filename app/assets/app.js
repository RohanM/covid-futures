import { bb, line } from 'billboard.js';
import "billboard.js/dist/billboard.css";

import "tailwindcss/tailwind.css"

window.onload = () => {
  document.querySelectorAll('.graph').forEach((graph) => {
    const state = graph.dataset.state;
    const series = JSON.parse(graph.dataset.series);
    const maxY = parseInt(graph.dataset.maxY);

    const xs = Object.fromEntries(
      series.map(s => [s.name, `${s.name}_x`])
    );

    const columns = series.map((s) => {
      return [
        [`${s.name}_x`].concat(s.labels),
        [s.name].concat(s.values),
      ];
    }).flat();

    var chart = bb.generate({
      bindto: `#graph-${state}`,
      data: {
        type: line(),
        xFormat: "%Y-%m-%d",
        xs: xs,
        columns: columns,
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
