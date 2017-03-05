Centralina livello 1
====================

Per il file "/var/www/dygraph-combined.js", fate riferimento al sito web: http://dygraphs.com/
(https://github.com/danvk/dygraphs/blob/master/LICENSE.txt)

Per l'avvio del "/etc/rc.local" con il "systemd" ho dovuto metter mano a qualche
impostazione, mi sono wscritto tutto qua: http://trance.myftp.org/3ns/content/etcrclocal-systemd


MEMO:

Comandi usati per copia su repository git:
  cp -varpu --parents /var/www/ .
  cp -varpu --parents /etc/nginx/dokuwiki* /etc/nginx/fcgiwrap.conf /etc/nginx/sites-available/level1 /etc/nginx/sites-enabled/level1 .
  cp -varpu --parents /etc/rc.local .
  cp -varpu --parents /etc/systemd/system/rc-local.service .
  cp -varpu --parents /etc/cron.hourly/mqtt2redis_check .
