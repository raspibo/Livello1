Centralina livello 1
====================

cp -varp /var/www/ .
cp -varp --parents /etc/nginx/dokuwiki* /etc/nginx/fcgiwrap.conf /etc/nginx/sites-available/level1 /etc/nginx/sites-enabled/level1 .

Per il file "/var/www/dygraph-combined.js", fate riferimento al sito web: http://dygraphs.com/
(https://github.com/danvk/dygraphs/blob/master/LICENSE.txt)