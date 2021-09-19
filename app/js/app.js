import { bb, line } from 'billboard.js';
import "billboard.js/dist/billboard.css";

window.onload = () => {
  const labels = JSON.parse(document.getElementById('graph-vic').dataset.labels);
  const values = JSON.parse(document.getElementById('graph-vic').dataset.values);

  var chart = bb.generate({
    bindto: "#graph-vic",
    data: {
      type: line(),
      x: 'Date',
      xFormat: "%Y-%m-%d",
      columns: [
        ["Date"].concat(labels),
        ["Cases"].concat(values),
      ],
    },
    axis: {
      x: {
        type: 'timeseries',
        tick: {
          format: '%e %b %Y',
        },
      },
    },
  });
};
