const path = require('path');

module.exports = {
  entry: './app/js/app.js',
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'app', 'static'),
  },
  devtool: 'eval-source-map',
  watch: true,
};
