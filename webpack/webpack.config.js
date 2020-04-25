'use strict';

const path = require('path');

const ManifestPlugin = require('webpack-manifest-plugin');

module.exports = {
  entry: './frontend/js/index.js',
  output: {
    filename: 'static/js/[name].[contenthash].js',
    path: path.resolve(__dirname, '..', 'app'),
  },
  plugins: [
      new ManifestPlugin({
        fileName: 'static/webpack-manifest.json',
        map: (file) => {
            file.path = file.path.replace(/static\//, '');
            return file;
        },
    }),
  ],
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
};
