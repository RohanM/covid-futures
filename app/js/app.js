import * as rv from 'rough-viz/dist/roughviz.min'

window.onload = () => {
  const values = JSON.parse(document.getElementById('graph-vic').dataset.values);

  new rv.Line({
    element: '#graph-vic',
    data: {
      cases: values,
    },
    width: window.innerWidth/2,
    roughness: 0,
    strokeWidth: 1,
    circle: false,
    interactive: false,
    xLabel: 'Date',
    yLabel: 'Cases',
    legend: false,
    title: 'Victoria',
  });
};
