const path = require('path');

module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },

  entry: './app/js/app.js',
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'app', 'static'),
  },

  devtool: 'eval-source-map',
  watch: true,
};
