Centralina livello 1
====================

Per il file "/var/www/dygraph-combined.js", fate riferimento al sito web: http://dygraphs.com/
(https://github.com/danvk/dygraphs/blob/master/LICENSE.txt)

Per l'avvio del "/etc/rc.local" con il "systemd" ho dovuto metter mano a qualche
impostazione, mi sono scritto tutto qua: http://trance.myftp.org/3ns/content/etcrclocal-systemd

Se installete/utilizzate anche il bot per Telegram (https://github.com/raspibo/bot4livello1),
copiatelo nella directory che preferite, e modificate il file /etc/cron.hourly/bot4livello1_check,
dove c'e` il (change directory) "cd /home/pi/projects/csv2image2telegram", mettete il vostro percorso.


MEMO's:

Programmi installati (necessari, utili e inutili):
  apt-file
  mc
  redis-server
  redis-tools
  python3-redis
  mosquitto
  paho-mqtt
  nginx
  fcgiwrap
  git
  ssl-cert (che poi non ho riconfigurato)
  php5-fpm (serve a  dokuwiki ?)

Comandi usati per copia su repository git:
  cp -varpu --parents /var/www/ .
  cp -varpu --parents /etc/nginx/dokuwiki* /etc/nginx/fcgiwrap.conf /etc/nginx/sites-available/level1 /etc/nginx/sites-enabled/level1 .
  cp -varpu --parents /etc/rc.local .
  cp -varpu --parents /etc/systemd/system/rc-local.service .
  cp -varpu --parents /etc/cron.hourly/mqtt2redis_check .
  cp -varpu --parents /etc/cron.hourly/bot4livello1_check .
