'use strict';

const path = require('path');
const glob = require('glob');

const ManifestPlugin = require('webpack-manifest-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const PurgecssPlugin = require('purgecss-webpack-plugin');
const LiveReloadPlugin = require('webpack-livereload-plugin');

const ENVIRONMENT = process.env.ENVIRONMENT;

// we don't want to use content hashed file names in development otherwise we'll end up
// with a million files when we're running webpack watch.
const staticNameFormat = ENVIRONMENT === 'development' ? '[name]' : '[name].[contenthash]'

module.exports = {
  mode: 'production',
  entry: [
    './frontend/js/index.js',
    './frontend/scss/main.scss',
  ],
  output: {
    filename: `static/js/${staticNameFormat}.js`,
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
          },
          {
            loader: 'postcss-loader',
            options: {
              config: {
                path: './webpack',
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
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
        filename: `static/css/${staticNameFormat}.css`,
        path: path.resolve(__dirname, '..', 'app'),
      }),
      new PurgecssPlugin({
        paths: glob.sync(`${path.join(__dirname, '..', 'app')}/**/*`,  { nodir: true }),
      }),
      new LiveReloadPlugin({
        // because we're not using hashed file names when running webpack watch we need to check hashes here.
        useSourceHash: true,
      }),
  ],
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
  watchOptions: {
    ignored: /node_modules/,
  },
};
