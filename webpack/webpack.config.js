'use strict';

const path = require('path');
const glob = require('glob');

const ManifestPlugin = require('webpack-manifest-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const PurgecssPlugin = require('purgecss-webpack-plugin');

module.exports = {
  mode: 'production',
  entry: [
    './frontend/js/index.js',
    './frontend/scss/main.scss',
  ],
  output: {
    filename: 'static/js/[name].[contenthash].js',
    path: path.resolve(__dirname, '..', 'app'),
  },
  module: {
    rules: [
      {
        test: /\.(scss|css)$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              importLoaders: 2,
              sourceMap: true,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              sourceMap: true,
              config: {
                path: './webpack',
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
              sassOptions: {
                outputStyle: 'compressed',
              }
            },
          },
        ],
      },
    ],
  },
  plugins: [
      new ManifestPlugin({
        fileName: 'static/webpack-manifest.json',
        map: (file) => {
            file.path = file.path.replace(/static\//, '');
            return file;
        },
      }),
      new MiniCssExtractPlugin({
        filename: 'static/css/[name].[contenthash].css',
        path: path.resolve(__dirname, '..', 'app'),
      }),
      new PurgecssPlugin({
        paths: glob.sync(`${path.join(__dirname, '..', 'app')}/**/*`,  { nodir: true }),
      }),
  ],
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
};
