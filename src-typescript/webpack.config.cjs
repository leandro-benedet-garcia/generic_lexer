const packageJSON = require("./package.json");

const path = require("path");

const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');


module.exports = {
    mode: "development",
    entry: {
        "errors": path.join(__dirname, "src", "rosetta-lang", "errors", "index.ts"),
        "ast": path.join(__dirname, "src", "rosetta-lang", "ast", "index.ts"),
        "main": path.join(__dirname, packageJSON.main)
    },
    devtool: "source-map",
    devServer: {
        compress: true,
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader'
            }
        ],
    },
    plugins: [
        new CleanWebpackPlugin(),
        new HtmlWebpackPlugin({
            xhtml: true,
            title: packageJSON.name
        }),
    ],
    output: {
        path: path.join(__dirname, "dist"),
        publicPath: "/dist/",
        filename: "[name].bundle.js"
    },
    resolve: {
        extensions: [".json", ".tsx", ".ts", ".html", ".js"]
    }
};
