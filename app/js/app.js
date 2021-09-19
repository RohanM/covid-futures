import { bb, line } from 'billboard.js';
import "billboard.js/dist/billboard.css";

window.onload = () => {
  const values = JSON.parse(document.getElementById('graph-vic').dataset.values);

  var chart = bb.generate({
    bindto: "#graph-vic",
    data: {
      type: line(),
      columns: [
        ["Cases"] + values,
      ]
    },
  });
};
