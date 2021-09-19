import * as rv from 'rough-viz/dist/roughviz.min'

window.onload = () => {
  new rv.Bar({
    element: '#viz0',
    data: 'https://raw.githubusercontent.com/jwilber/random_data/master/flavors.csv',
    labels: 'flavor',
    values: 'price'
  });
};
