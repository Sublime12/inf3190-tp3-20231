let mix = require('laravel-mix');

mix.setPublicPath('static/')
    .js('assets/app.js', 'js')
    .postCss('assets/app.css', 'css', [
        require('tailwindcss'),
    ])
;