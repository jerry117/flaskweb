'use strict'
const { resolve } = require('path')
const path = require('path')
const { listenerCount } = require('process')
const defaultSettings = require('./src/settings.js')


const name = defaultSettings.title || 'app'


module.exports = {
    publicPath: '/',
    outputDir: 'dist',
    assetsDir: 'static',

    lintOnSave: false,
    productionSourceMap: false,

    devServer: {
        host: '0.0.0.0',
        port: 8080,
        proxy: {
            '/auth/': {
                target: 'http://localhost:5000',
                changeOrigin: true,
            }
        },
    },

    configureWebpack: {
        name: name,
        resolve: {
            alias: {
                '@': resolve('src')

            }
        },

    },

    // chainWebpack(config) {
    //     config.plugin('preload').tap( () => [
    //         {
    //             rel: 'preload',
    //             fileBlacklist: [/\.map$/, /hot-update\.js$/, /runtime\..*\.js$/],
    //             include: 'initial'
    //         }
    //     ] )

    //     config.plugins.delete('prefetch')

    //     config.module
    //         .rule('svg')
    //         .exclude.add(resolve('src/icons'))
    //         .end()
    // }
}



