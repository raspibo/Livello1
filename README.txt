Centralina livello 1
====================

Per il file "/var/www/dygraph.min.js", fate riferimento al sito web: http://dygraphs.com/
(https://github.com/danvk/dygraphs/blob/master/LICENSE.txt)

Se installete/utilizzate anche il bot per Telegram (https://github.com/raspibo/bot4livello1),
copiatelo nella directory che preferite, e modificate il file /etc/cron.hourly/bot4livello1_check,
dove c'e` il (change directory) "cd /home/pi/projects/csv2image2telegram", mettete il vostro percorso.


MEMO's:

Programmi installati (necessari, utili e inutili):
  nginx
  fcgiwrap
  redis-server
  python3-redis
  mosquitto
  paho-mqtt
  ssl-cert
  php-fpm
  php7.0-xml
  python3-pip
  python3-pandas
  paho-mqtt (pip3 install)
  python-telegram-bot (pip3 ")
  pygal (pip3 ")
  git
  mosquitto-clients
  dokuwiki (manual install)
  apt-file
  mc
  redis-tools
  aria2

Comando per visualizzare i dati in arrivo MQTT (tutti i topic, dalla root):
  mosquitto_sub -v -t \#

Comandi usati per copia su repository git:
  cp -vapu --parents /var/www/ .
  cp -vapu --parents /etc/nginx/dokuwiki* /etc/nginx/fcgiwrap.conf /etc/nginx/sites-available/level1 /etc/nginx/sites-enabled/level1 .
  cp -vapu --parents /etc/rc.local .
  cp -vapu --parents /etc/cron.hourly/*_check .
  cp -vapu --parents /etc/cron.monthly/dokuwiki .
  cp -vapu --parents /etc/cron.daily/backupredis .
