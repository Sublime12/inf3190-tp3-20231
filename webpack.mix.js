let mix = require('laravel-mix');

mix.js('assets/app.js', 'js').setPublicPath('static/');

mix.postCss('assets/app.css', 'css');