const path = require("path");

const webpack = require('webpack');

const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

const devMode = process.env.NODE_ENV !== 'production'

module.exports = {
  context: __dirname,

  entry: './frontend/js/index.js',

  output: {
      filename: devMode ? '[name].js' : '[name].[contenthash].js',
      chunkFilename: devMode ? '[id].js' : '[id].[contenthash].js',
      path: path.resolve('./app/app/static/bundles/'),
  },

  optimization: {
    minimizer: [
      new UglifyJsPlugin({
        cache: true,
        parallel: true,
        sourceMap: true // set to true if you want JS source maps
      }),
      new OptimizeCSSAssetsPlugin({})
    ]
  },

  plugins: [
    new BundleTracker({filename: './app/webpack-stats.json'}),
    new MiniCssExtractPlugin({
      filename: devMode ? '[name].css' : '[name].[contenthash].css',
      chunkFilename: devMode ? '[id].css' : '[id].[contenthash].css',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', '.css', '.scss']
  },


};