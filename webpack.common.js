const path = require('path');

module.exports = {
  entry: './app/assets/app.js',
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'app', 'static'),
  },

  module: {
    rules: [
      {
        test: /\.(js)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
    ],
  },
};
