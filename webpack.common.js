const path = require('path');

module.exports = {
  entry: './src/app/assets/app.js',
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'src', 'app', 'static'),
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
