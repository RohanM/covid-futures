const path = require('path');

module.exports = {
  entry: './app/js/app.js',
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'app', 'static'),
  },

  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
};
